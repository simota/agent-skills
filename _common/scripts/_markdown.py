"""Small Markdown masks shared by checks that must distinguish prose from examples."""

from __future__ import annotations

import re


INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)", re.DOTALL)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def without_inline_code(text: str) -> str:
    """Hide code spans without changing offsets or line positions."""
    return INLINE_CODE.sub(lambda match: re.sub(r"[^\n]", " ", match.group()), text)


def without_fenced_examples(text: str) -> str:
    """Mask fenced examples while retaining source lines and HTML comments.

    A backtick fence cannot contain backticks in its info string. Four-space
    indentation is a separate code block, and fence-shaped text inside an HTML
    comment does not start a fenced block in the surrounding document.
    """
    lines = []
    fence = ""
    in_comment = False
    for line in text.splitlines():
        marker = FENCE.match(line)
        if fence:
            if (marker and marker.group(1)[0] == fence[0]
                    and len(marker.group(1)) >= len(fence) and not marker.group(2).strip()):
                fence = ""
            lines.append("")
            continue
        if (not in_comment and marker
                and (marker.group(1)[0] == "~" or "`" not in marker.group(2))):
            fence = marker.group(1)
            lines.append("")
            continue
        lines.append(line)
        if not in_comment and line.startswith(("    ", "\t")):
            continue
        comment_text = without_inline_code(line)
        position = 0
        while True:
            token = "-->" if in_comment else "<!--"
            start = comment_text.find(token, position)
            if start == -1:
                break
            in_comment = not in_comment
            position = start + len(token)
    return "\n".join(lines)


def without_html_comments(text: str) -> str:
    """Mask HTML comments, preserving comment-like strings in code and offsets."""
    original_lines = text.split("\n")
    visible_lines = without_fenced_examples(text).split("\n")
    visible_lines.extend([""] * (len(original_lines) - len(visible_lines)))
    visible = "\n".join(line.ljust(len(original))
                        for original, line in zip(original_lines, visible_lines))
    result = list(text)
    # Match comments and code spans in source order. Masking code spans first
    # lets an unmatched backtick *inside* a comment consume its closing marker
    # and a later, unrelated code span in the live document.
    # Inline spans cannot bridge a blank-line paragraph boundary. A literal
    # unmatched backtick in one paragraph must not hide comments in another.
    inline = r"(?<!`)(`+)(?!`)((?:(?!\n[ \t]*\n).)*?)(?<!`)\1(?!`)"
    tokens = re.compile(r"<!--.*?(?:-->|\Z)|" + inline, re.DOTALL)
    for match in tokens.finditer(visible):
        if not match.group().startswith("<!--"):
            continue
        result[match.start():match.end()] = [
            "\n" if char == "\n" else " " for char in text[match.start():match.end()]
        ]
    return "".join(result)


def markdown_section(text: str, title: str, *, allow_suffix: bool = False) -> str | None:
    """Read an active level-two section, retaining its literal example blocks."""
    # ATX headings are block syntax; an unmatched inline backtick in preceding
    # prose cannot swallow one. Fences/comments are the relevant exclusions.
    visible = without_fenced_examples(without_html_comments(text))
    lines = []
    found = False
    for original, line in zip(text.splitlines(), visible.splitlines()):
        heading = re.match(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$", line)
        if heading and len(heading.group(1)) <= 2:
            if found:
                break
            name = heading.group(2)
            found = len(heading.group(1)) == 2 and (
                name == title or allow_suffix and name.startswith(title + " ")
            )
            continue
        if found:
            lines.append(original)
    return "\n".join(lines) if found else None


def fenced_blocks(text: str):
    """Yield active fenced-block bodies, accepting backticks and tilde fences."""
    fence = ""
    lines = []
    for line in without_html_comments(text).splitlines():
        marker = FENCE.match(line)
        if fence:
            if (marker and marker.group(1)[0] == fence[0]
                    and len(marker.group(1)) >= len(fence) and not marker.group(2).strip()):
                yield "\n".join(lines)
                fence = ""
                lines = []
            else:
                lines.append(line)
        elif marker and (marker.group(1)[0] == "~" or "`" not in marker.group(2)):
            fence = marker.group(1)
    if fence:
        yield "\n".join(lines)
