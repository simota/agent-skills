"""Regression coverage for repository fixture isolation."""

import tempfile
import unittest
from pathlib import Path

from test_checkers import copy_repository


class TestRepositoryCopy(unittest.TestCase):
    def test_temp_directory_inside_source_does_not_copy_itself(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("fixture", encoding="utf-8")
            archive = source / ".archive"
            archive.mkdir()
            (archive / "old.md").write_text("history", encoding="utf-8")
            stale_fixture = source / "checker-tests-interrupted"
            stale_fixture.mkdir()
            (stale_fixture / "partial.md").write_text("partial copy", encoding="utf-8")
            (source / "link.md").symlink_to("SKILL.md")
            temporary_root = source / "nested" / "checker-tests"
            temporary_root.mkdir(parents=True)
            destination = temporary_root / "repo"

            copy_repository(source, destination, temporary_root)

            self.assertEqual((destination / "SKILL.md").read_text(), "fixture")
            self.assertEqual((destination / ".archive/old.md").read_text(), "history")
            self.assertTrue((destination / "link.md").is_symlink())
            self.assertFalse((destination / "nested/checker-tests").exists())
            self.assertFalse((destination / "checker-tests-interrupted").exists())


if __name__ == "__main__":
    unittest.main()
