"""Execute documented shell helpers against representative filesystem inputs."""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
BLOCKS = re.findall(
    r"```bash\n(.*?)\n```", (REPO / "_common/PORTABILITY.md").read_text(), re.S
)


class TestPortableHelpers(unittest.TestCase):
    def run_helper(self, name, command, *args, setup=""):
        definition = next(block for block in BLOCKS if name + "()" in block)
        return subprocess.run(
            ["bash", "-c", definition + "\n" + setup + "\n" + command, "test", *args],
            capture_output=True, timeout=10,
        )

    def test_mtime_is_one_epoch_value(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "file with spaces"
            path.touch()
            os.utime(path, (1700000000, 1700000000))
            result = self.run_helper("file_mtime", 'file_mtime "$1"', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, b"1700000000\n")

    def test_missing_mtime_keeps_documented_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_helper("file_mtime", 'file_mtime "$1"', directory + "/missing")
            self.assertEqual(result.stdout, b"0\n")

    def test_find_preserves_newlines_and_deduplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory) / "line\nbreak"
            parent.mkdir()
            (parent / "one.md").touch()
            (parent / "two.md").touch()
            result = self.run_helper(
                "find_dirs_with_file", 'find_dirs_with_file "$1" "*.md"', directory
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, os.fsencode(parent) + b"\0")

    def test_search_recurses_with_native_grep_and_perl(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "match.txt"
            path.parent.mkdir()
            path.write_text("prefix123\n")
            for setup in ("", "grep() { return 2; }"):
                with self.subTest(setup=setup):
                    result = self.run_helper(
                        "pcre_search", 'pcre_search "(?<=prefix)[0-9]+" "$1"',
                        directory, setup=setup,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, os.fsencode(path) + b"\n")

    def test_perl_search_no_match_is_not_success(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_helper(
                "pcre_search", 'pcre_search "absent" "$1"', directory,
                setup="grep() { return 2; }",
            )
            self.assertEqual(result.returncode, 1, result.stderr)

    def test_search_option_like_pattern_and_explicit_directory_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            (target / "match.txt").write_text("-literal\n")
            alias = root / "alias"
            alias.symlink_to(target, target_is_directory=True)
            (target / "cycle").symlink_to(target, target_is_directory=True)
            for setup in ("", "grep() { return 2; }"):
                with self.subTest(setup=setup):
                    result = self.run_helper(
                        "pcre_search", 'pcre_search "-literal" "$1"', str(alias),
                        setup=setup,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, os.fsencode(alias / "match.txt") + b"\n")

    def test_perl_search_reports_missing_file_and_invalid_pattern(self):
        with tempfile.TemporaryDirectory() as directory:
            for pattern in ("x", "["):
                with self.subTest(pattern=pattern):
                    result = self.run_helper(
                        "pcre_search", 'pcre_search "$1" "$2"', pattern,
                        directory + "/missing", setup="grep() { return 2; }",
                    )
                    self.assertEqual(result.returncode, 2, result.stderr)

    def test_perl_timeout_preserves_child_signal_status(self):
        result = self.run_helper(
            "run_with_timeout", "run_with_timeout 3 sh -c 'kill -TERM $$'",
            setup="command() { return 1; }",
        )
        self.assertEqual(result.returncode, 143, result.stderr)

    def test_perl_timeout_preserves_regular_failure(self):
        result = self.run_helper(
            "run_with_timeout", "run_with_timeout 3 sh -c 'exit 7'",
            setup="command() { return 1; }",
        )
        self.assertEqual(result.returncode, 7, result.stderr)

    def test_perl_timeout_stops_descendants(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "late-write"
            result = self.run_helper(
                "run_with_timeout",
                '''run_with_timeout 1 sh -c '(sleep 2; touch "$1") & wait' sh "$1"''',
                str(marker), setup="command() { return 1; }",
            )
            self.assertEqual(result.returncode, 124, result.stderr)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
