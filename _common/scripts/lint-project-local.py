#!/usr/bin/env python3
"""Validate project-local skill mirroring and shared-reference delivery."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_REL = Path(".claude/skills")
MIRROR_REL = Path(".agents/skills")
REGISTRY_REL = Path("_common/PROJECT_LOCAL_SKILLS.md")
SHARED_NAMESPACES = ("_common", "_templates")

REGISTRY_ROW_RE = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|", re.MULTILINE)
SHARED_REF_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"((?:_common|_templates)/[A-Za-z0-9_./-]+\.(?:md|py|json|ya?ml))"
)


@dataclass(frozen=True)
class Finding:
    priority: str
    rule: str
    message: str


def _registry_names(repo_root: Path) -> set[str] | None:
    path = repo_root / REGISTRY_REL
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if "## Registry" not in text:
        return set()
    section = text.split("## Registry", 1)[1].split("\n## ", 1)[0]
    return set(REGISTRY_ROW_RE.findall(section))


def _skill_dirs(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        return {}
    result: dict[str, Path] = {}
    for entry in sorted(root.iterdir(), key=lambda path: path.name):
        if entry.name.startswith(".") or entry.is_symlink() or not entry.is_dir():
            continue
        if (entry / "SKILL.md").is_file():
            result[entry.name] = entry
    return result


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _manifest(root: Path) -> dict[str, tuple[str, str]]:
    """Return a recursive manifest without following directory symlinks."""
    manifest: dict[str, tuple[str, str]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)

        for name in list(dirnames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                manifest[rel] = ("symlink", os.readlink(path))
                dirnames.remove(name)
            else:
                manifest[rel] = ("dir", "")

        for name in filenames:
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                manifest[rel] = ("symlink", os.readlink(path))
            else:
                manifest[rel] = ("file", _digest(path))

    return manifest


def _markdown_text(skill_dir: Path) -> str:
    chunks: list[str] = []
    for dirpath, dirnames, filenames in os.walk(skill_dir, followlinks=False):
        base = Path(dirpath)
        dirnames[:] = [name for name in dirnames if not (base / name).is_symlink()]
        for name in filenames:
            path = base / name
            if path.suffix.lower() == ".md" and not path.is_symlink():
                chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def _shared_refs(skill_dir: Path) -> set[str]:
    return set(SHARED_REF_RE.findall(_markdown_text(skill_dir)))


def _format_set(values: set[str]) -> str:
    return ", ".join(sorted(values)) if values else "(none)"


def _check_shared_delivery(
    repo_root: Path,
    skill_name: str,
    canonical_dir: Path,
    mirror_dir: Path,
    findings: list[Finding],
) -> None:
    refs = sorted(_shared_refs(canonical_dir))
    if not refs:
        return

    for namespace in SHARED_NAMESPACES:
        namespace_refs = [ref for ref in refs if ref.startswith(f"{namespace}/")]
        if not namespace_refs:
            continue

        expected = (repo_root / namespace).resolve()
        for label, skill_dir in (("canonical", canonical_dir), ("mirror", mirror_dir)):
            link = skill_dir / namespace
            if not link.is_symlink():
                findings.append(
                    Finding(
                        "P0",
                        "PL-3",
                        f"{skill_name}: {label} copy references `{namespace}/` "
                        f"but `{link.relative_to(repo_root)}` is not a symlink",
                    )
                )
                continue

            try:
                resolved = link.resolve(strict=True)
            except (FileNotFoundError, RuntimeError, OSError) as exc:
                findings.append(
                    Finding(
                        "P0",
                        "PL-3",
                        f"{skill_name}: {label} `{link.relative_to(repo_root)}` "
                        f"does not resolve: {exc}",
                    )
                )
                continue

            if resolved != expected:
                findings.append(
                    Finding(
                        "P0",
                        "PL-3",
                        f"{skill_name}: {label} `{link.relative_to(repo_root)}` "
                        f"resolves to `{resolved}`, expected `{expected}`",
                    )
                )
                continue

            for ref in namespace_refs:
                if not (skill_dir / ref).is_file():
                    findings.append(
                        Finding(
                            "P1",
                            "PL-3",
                            f"{skill_name}: {label} reference `{ref}` does not resolve",
                        )
                    )


def check(repo_root: Path = REPO_ROOT) -> list[Finding]:
    findings: list[Finding] = []
    canonical_root = repo_root / CANONICAL_REL
    mirror_root = repo_root / MIRROR_REL

    for label, root in (("canonical", canonical_root), ("mirror", mirror_root)):
        if not root.is_dir():
            findings.append(
                Finding(
                    "P0",
                    "PL-1",
                    f"{label} project-local root `{root.relative_to(repo_root)}` is missing",
                )
            )

    registry = _registry_names(repo_root)
    if registry is None:
        findings.append(
            Finding("P0", "PL-1", f"project-local registry `{REGISTRY_REL}` is missing")
        )
        registry = set()
    elif not registry:
        findings.append(
            Finding(
                "P1",
                "PL-1",
                f"project-local registry `{REGISTRY_REL}` has no skill rows",
            )
        )

    canonical = _skill_dirs(canonical_root)
    mirror = _skill_dirs(mirror_root)
    canonical_names = set(canonical)
    mirror_names = set(mirror)

    if registry and (canonical_names != registry or mirror_names != registry):
        findings.append(
            Finding(
                "P0",
                "PL-1",
                "project-local roster differs from registry: "
                f"registry=[{_format_set(registry)}], "
                f"canonical=[{_format_set(canonical_names)}], "
                f"mirror=[{_format_set(mirror_names)}]",
            )
        )
    elif canonical_names != mirror_names:
        findings.append(
            Finding(
                "P0",
                "PL-1",
                "canonical/mirror project-local rosters differ: "
                f"canonical=[{_format_set(canonical_names)}], "
                f"mirror=[{_format_set(mirror_names)}]",
            )
        )

    for skill_name in sorted(canonical_names & mirror_names):
        canonical_dir = canonical[skill_name]
        mirror_dir = mirror[skill_name]

        canonical_manifest = _manifest(canonical_dir)
        mirror_manifest = _manifest(mirror_dir)
        if canonical_manifest != mirror_manifest:
            differing = sorted(
                path
                for path in set(canonical_manifest) | set(mirror_manifest)
                if canonical_manifest.get(path) != mirror_manifest.get(path)
            )
            preview = ", ".join(differing[:8])
            if len(differing) > 8:
                preview += f", ... (+{len(differing) - 8})"
            findings.append(
                Finding(
                    "P0",
                    "PL-2",
                    f"{skill_name}: canonical/mirror trees differ at {preview}",
                )
            )

        _check_shared_delivery(
            repo_root, skill_name, canonical_dir, mirror_dir, findings
        )

    return findings


def _should_fail(findings: list[Finding], severity: str) -> bool:
    if severity == "warning":
        return False
    if severity == "error":
        return any(finding.priority in {"P0", "P1"} for finding in findings)
    return bool(findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate project-local skill mirroring and shared references."
    )
    parser.add_argument(
        "--severity",
        choices=("warning", "error", "strict"),
        default="warning",
        help="warning reports only; error blocks P0/P1; strict blocks any finding",
    )
    args = parser.parse_args(argv)

    findings = check()
    for finding in findings:
        print(f"[{finding.priority}] {finding.rule}: {finding.message}")

    if not findings:
        count = len(_skill_dirs(REPO_ROOT / CANONICAL_REL))
        print(
            f"project-local validation OK: {count} skills mirrored and shared refs resolved"
        )

    return 1 if _should_fail(findings, args.severity) else 0


if __name__ == "__main__":
    sys.exit(main())
