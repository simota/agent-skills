"""Shared parsing for the validator and the published Recipe directory."""

from __future__ import annotations

import re

from _markdown import fenced_blocks, markdown_section, without_fenced_examples, without_html_comments

REGISTRY = re.compile(r"`(reference/[a-z0-9-]*recipes?-index\.md)`")


def active_text(text: str) -> str:
    return without_fenced_examples(without_html_comments(text))


def recipe_section(text: str) -> str | None:
    return markdown_section(text, "Recipes")


def registry_pointer(block: str) -> str | None:
    match = REGISTRY.search(active_text(block))
    return match.group(1) if match else None


def recipe_cells(block: str):
    """Yield Recipe table rows, respecting escaped pipes inside Markdown cells."""
    in_table = False
    for line in active_text(block).splitlines():
        if not line.lstrip().startswith("|"):
            in_table = False
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip())]
        cells = cells[1:]
        if cells and not cells[-1]:
            cells.pop()
        if not in_table:
            in_table = len(cells) >= 2 and cells[0].lower() == "recipe" \
                and cells[1].lower() == "subcommand"
            continue
        if cells and re.fullmatch(r":?-+:?", cells[0]):
            continue
        yield cells or [""]


def dispatch_allowlist(block: str) -> list[str] | None:
    """Read the registry's explicitly labelled allowlist, keeping duplicate tokens."""
    marker = re.search(r"\bdispatch allowlist(?: only)?\b", active_text(block), re.IGNORECASE)
    if marker is None:
        return None
    # Locate the label in the original block: fence masking preserves lines but
    # deliberately drops their widths, so masked character offsets cannot be used.
    lines = block.splitlines()
    label_line = active_text(block)[:marker.start()].count("\n")
    body = next(fenced_blocks("\n".join(lines[label_line:])), None)
    return [token.rstrip("*★") for token in re.findall(r"[^\s·]+", body)] \
        if body is not None else None
