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
