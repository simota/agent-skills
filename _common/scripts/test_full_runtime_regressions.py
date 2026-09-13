#!/usr/bin/env python3
"""Behavioral regressions for report output integrity and kit rendering."""

import re
import shutil
import unittest

from test_launch_regressions import BASH, NODE, ROOT, CliFixtures


def small_pdf():
    """A complete one-page PDF, deliberately smaller than 1000 bytes."""
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>",
               b"<< /Type /Pages /Count 1 /Kids [3 0 R] >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>"]
    result = b"%PDF-1.4\n"
    offsets = []
    for index, body in enumerate(objects, 1):
        offsets.append(len(result))
        result += f"{index} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(result)
    result += b"xref\n0 4\n0000000000 65535 f \n"
    result += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets)
    result += f"trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return result


@unittest.skipUnless(NODE, "Node.js is required")
class ReportAttributeRegressions(CliFixtures):
    def test_single_quoted_template_attribute_cannot_be_escaped(self):
        self.executable("gh", "print('[]')\n")
        template = self.work / "custom.html"
        template.write_text("<p data-author='{{AUTHOR}}'>{{AUTHOR}}</p>")
        result = self.run_cli([NODE, str(ROOT / "launch/scripts/generate-report.js"),
                              "--repo", "owner/repo", "--author", "' onmouseover='alert(1)",
                              "--template", str(template), "--output", "report.html"])
        self.assertEqual(result.returncode, 0, result.stderr)
        html = (self.work / "report.html").read_text()
        self.assertIn("data-author='&#39; onmouseover=&#39;alert(1)'", html)
        self.assertNotIn("data-author='' onmouseover=", html)


@unittest.skipUnless(BASH, "Bash is required")
class PdfIntegrityRegressions(CliFixtures):
    def setUp(self):
        super().setUp()
        self.input = self.work / "input.html"
        self.input.write_text("<html>fixture</html>")
        self.output = self.work / "output.pdf"
        self.fixture = self.work / "fixture.pdf"
        self.env["PDF_FIXTURE"] = str(self.fixture)
        self.executable("google-chrome", """import os, shutil, sys
output = next(arg.split('=', 1)[1] for arg in sys.argv if arg.startswith('--print-to-pdf='))
shutil.copyfile(os.environ['PDF_FIXTURE'], output)
""")

    def convert(self):
        return self.run_cli([BASH, str(ROOT / "launch/scripts/html-to-pdf.sh"),
                             "--method", "chrome", str(self.input), str(self.output)])

    def test_valid_small_pdf_is_published(self):
        self.fixture.write_bytes(small_pdf())
        self.assertLess(self.fixture.stat().st_size, 1000)
        result = self.convert()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_bytes(), small_pdf())

    def test_truncated_pdf_does_not_replace_existing_output(self):
        self.fixture.write_bytes(b"%PDF-1.4\n" + b"truncated object\n" * 100)
        self.output.write_bytes(small_pdf())
        result = self.convert()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), small_pdf())


@unittest.skipUnless(NODE, "Node.js is required")
class PuppeteerPublicationRegressions(CliFixtures):
    def setUp(self):
        super().setUp()
        self.input = self.work / "input.html"
        self.input.write_text("<html>fixture</html>")
        self.output = self.work / "output.pdf"
        self.output.write_bytes(small_pdf())
        module = self.work / "node_modules/puppeteer"
        module.mkdir(parents=True)
        self.env["NODE_PATH"] = str(module.parent)
        (module / "index.js").write_text("""
const fs = require('fs');
module.exports.launch = async () => ({
  async newPage() { return {
    async goto() {}, async evaluate() {},
    async pdf(options) {
      fs.writeFileSync(options.path, '%PDF-1.7\\nnew report\\n%%EOF\\n');
      if (process.env.PDF_FAIL === 'print') throw Error('print failed after writing');
    }
  }; },
  async close() { if (process.env.PDF_FAIL === 'close') throw Error('close failed'); }
});
""")

    def convert(self):
        return self.run_cli([NODE, str(ROOT / "launch/scripts/puppeteer-pdf.js"),
                             str(self.input), str(self.output)])

    def test_failed_print_preserves_previous_report(self):
        self.env["PDF_FAIL"] = "print"
        result = self.convert()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), small_pdf())
        self.assertEqual(list(self.work.glob(".puppeteer-pdf.*")), [])

    def test_browser_close_failure_does_not_publish_or_report_success(self):
        self.env["PDF_FAIL"] = "close"
        result = self.convert()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.output.read_bytes(), small_pdf())
        self.assertNotIn("Done:", result.stdout)
        self.assertEqual(list(self.work.glob(".puppeteer-pdf.*")), [])

    def test_successful_print_replaces_previous_report(self):
        result = self.convert()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(b"new report", self.output.read_bytes())
        self.assertIn("Done:", result.stdout)
        self.assertEqual(list(self.work.glob(".puppeteer-pdf.*")), [])


@unittest.skipUnless(BASH, "Bash is required")
class LearningKitRenderRegressions(CliFixtures):
    def test_documented_copy_steps_keep_shared_contracts_reachable(self):
        source = self.work / "_templates/learning-loop-kit/base"
        shutil.copytree(ROOT / "_templates/learning-loop-kit/base", source, symlinks=True)
        shared = self.work / "_common"
        shared.mkdir()
        (shared / "OPUS_5_AUTHORING.md").write_text("shared contract")
        (self.work / "project").mkdir()
        readme = (ROOT / "_templates/learning-loop-kit/README.md").read_text()
        blocks = re.findall(r"```bash\n(.*?)```", readme, re.S)
        for prefix, destination in [("cp -RP _templates/learning-loop-kit/base", "_templates/demo-kit"),
                                    ("cp -RP _templates/<kit-slug>-kit", "project/review")]:
            block = next(block for block in blocks if block.strip().startswith(prefix))
            script = block.replace("<kit-slug>", "demo").replace("<project>", "project")
            result = self.run_cli([BASH, "-e", "-c", script.replace("<DOMAIN_DIR>", "review")])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((self.work / destination / "_common/OPUS_5_AUTHORING.md").read_text(),
                             "shared contract")

    def test_documented_render_with_empty_rules_passes_residue_gate(self):
        kit = self.work / "review-kit"
        shutil.copytree(ROOT / "_templates/learning-loop-kit/base", kit, symlinks=True)
        # Every config token is filled; the documented empty start removes the
        # seed entry and its index rows, but preserves reusable instructions.
        for path in kit.rglob("*.md"):
            text = re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: match[1].lower(), path.read_text())
            if path.name == "core.md":
                text = re.sub(r"^### .*?^---\n", "---\n", text, flags=re.M | re.S)
            elif path.name == "INDEX.md":
                text = "\n".join(line for line in text.splitlines() if "-CORE-example" not in line)
            path.write_text(text)
        result = self.run_cli([BASH, str(ROOT / "_templates/learning-loop-kit/_scripts/check-rendered.sh"),
                              str(kit)])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("is clean", result.stdout)


if __name__ == "__main__":
    unittest.main()
