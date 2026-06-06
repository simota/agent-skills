#!/usr/bin/env python3
"""Trim oversized reference files by truncating code blocks and verbose sections."""

import os
import re
import glob

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAX_CODE_BLOCK_LINES = 15
FILE_THRESHOLD = 400  # Only process files over this many lines

def trim_code_blocks(content):
    """Truncate code blocks longer than MAX_CODE_BLOCK_LINES."""
    lines = content.split('\n')
    result = []
    in_block = False
    block_lines = []
    block_lang = ""
    trimmed_count = 0

    for line in lines:
        if not in_block and line.startswith('```'):
            in_block = True
            block_lang = line[3:].strip()
            block_lines = [line]
        elif in_block and line.startswith('```'):
            # End of block
            in_block = False
            block_content = block_lines[1:]  # Exclude opening ```
            if len(block_content) > MAX_CODE_BLOCK_LINES:
                # Truncate
                trimmed_count += 1
                result.extend(block_lines[:MAX_CODE_BLOCK_LINES + 1])  # opening + N lines
                # Add truncation indicator based on language
                lang = block_lang.lower()
                if lang in ('html', 'xml', 'svg'):
                    result.append('<!-- ... -->')
                elif lang in ('css', 'scss', 'less'):
                    result.append('/* ... */')
                elif lang in ('python', 'py', 'ruby', 'rb', 'shell', 'bash', 'sh', 'yaml', 'yml', 'toml'):
                    result.append('# ...')
                elif lang in ('markdown', 'md', ''):
                    result.append('...')
                else:
                    result.append('// ...')
                result.append(line)  # closing ```
            else:
                result.extend(block_lines)
                result.append(line)
            block_lines = []
        elif in_block:
            block_lines.append(line)
        else:
            result.append(line)

    # Handle unclosed block
    if in_block:
        result.extend(block_lines)

    return '\n'.join(result), trimmed_count


def trim_verbose_tables(content):
    """Trim markdown tables with more than 20 data rows to 10 rows."""
    lines = content.split('\n')
    result = []
    table_rows = []
    in_table = False
    header_done = False
    trimmed = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        is_table_row = stripped.startswith('|') and stripped.endswith('|')
        is_separator = is_table_row and all(c in '| -:' for c in stripped)

        if is_table_row:
            if not in_table:
                in_table = True
                header_done = False
                table_rows = [line]
            elif not header_done and is_separator:
                header_done = True
                table_rows.append(line)
            else:
                table_rows.append(line)
        else:
            if in_table:
                # End of table
                header_count = 2 if header_done else 0
                data_rows = table_rows[header_count:]
                if len(data_rows) > 20:
                    trimmed += 1
                    result.extend(table_rows[:header_count])
                    result.extend(data_rows[:10])
                    result.append(f'| ... | ({len(data_rows) - 10} more rows) |')
                else:
                    result.extend(table_rows)
                in_table = False
                table_rows = []
            result.append(line)

    # Handle table at end of file
    if in_table:
        result.extend(table_rows)

    return '\n'.join(result), trimmed


def remove_legacy_sections(content):
    """Remove sections with 'Legacy' or 'Deprecated' in the heading."""
    lines = content.split('\n')
    result = []
    skip_level = 0
    removed = 0

    for line in lines:
        heading_match = re.match(r'^(#{1,4})\s+(.+)', line)

        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).lower()

            if skip_level > 0:
                if level <= skip_level:
                    # New section at same or higher level, stop skipping
                    skip_level = 0
                else:
                    continue

            if 'legacy' in title or 'deprecated' in title:
                skip_level = level
                removed += 1
                continue

        if skip_level > 0:
            continue

        result.append(line)

    return '\n'.join(result), removed


def process_file(filepath):
    """Process a single file and return stats."""
    with open(filepath, 'r') as f:
        content = f.read()

    original_lines = content.count('\n') + 1

    if original_lines <= FILE_THRESHOLD:
        return None

    content, blocks_trimmed = trim_code_blocks(content)
    content, tables_trimmed = trim_verbose_tables(content)
    content, sections_removed = remove_legacy_sections(content)

    # Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    new_lines = content.count('\n') + 1
    saved = original_lines - new_lines

    if saved > 5:  # Only write if meaningful savings
        with open(filepath, 'w') as f:
            f.write(content)
        return {
            'file': filepath,
            'before': original_lines,
            'after': new_lines,
            'saved': saved,
            'blocks': blocks_trimmed,
            'tables': tables_trimmed,
            'sections': sections_removed,
        }
    return None


def main():
    results = []
    total_saved = 0

    files = sorted(glob.glob(os.path.join(BASE, "*/reference/*.md")))
    print(f"Scanning {len(files)} reference files...\n")

    for filepath in files:
        result = process_file(filepath)
        if result:
            results.append(result)
            total_saved += result['saved']

    # Sort by savings
    results.sort(key=lambda r: r['saved'], reverse=True)

    print(f"{'File':<65} {'Before':>6} {'After':>6} {'Saved':>6} {'Blocks':>6}")
    print("-" * 95)
    for r in results:
        relpath = os.path.relpath(r['file'], BASE)
        print(f"{relpath:<65} {r['before']:>6} {r['after']:>6} {r['saved']:>6} {r['blocks']:>6}")

    print(f"\n{'='*95}")
    print(f"Files modified: {len(results)}")
    print(f"Total lines saved: {total_saved}")


if __name__ == "__main__":
    main()
