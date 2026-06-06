#!/usr/bin/env python3
"""Clean up redundant reference files and update SKILL.md references tables."""

import os
import re
import glob

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Files to delete (by basename)
DELETE_BASENAMES = [
    "interaction-triggers.md",
    "handoff-formats.md",
    "handoffs.md",
    "collaboration-handoffs.md",
    "agent-handoffs.md",
    "agent-collaboration.md",
    "inbound-handoffs.md",
]

# Titan-specific files to delete
TITAN_DELETE = [
    "titan/reference/guardrail-integration.md",
    "titan/reference/phase-context-scoring.md",
    "titan/reference/magi-protocol.md",
    "titan/reference/rally-coordination.md",
]

def delete_files():
    """Delete all redundant reference files."""
    deleted = []

    # Delete by basename pattern
    for basename in DELETE_BASENAMES:
        pattern = os.path.join(BASE, "*/reference", basename)
        for f in glob.glob(pattern):
            os.remove(f)
            deleted.append(f)

    # Delete Titan-specific files
    for f in TITAN_DELETE:
        path = os.path.join(BASE, f)
        if os.path.exists(path):
            os.remove(path)
            deleted.append(path)

    return deleted

def update_skill_references(skill_path, deleted_basenames):
    """Remove references to deleted files from SKILL.md."""
    with open(skill_path, 'r') as f:
        content = f.read()

    original = content

    # Remove table rows that reference deleted files
    for basename in deleted_basenames:
        # Match table rows like: | `reference/interaction-triggers.md` | ... |
        pattern = rf'\|[^\n]*`reference/{re.escape(basename)}`[^\n]*\|\n'
        content = re.sub(pattern, '', content)

        # Also match without backticks: | reference/interaction-triggers.md | ... |
        pattern2 = rf'\|[^\n]*reference/{re.escape(basename)}[^\n]*\|\n'
        content = re.sub(pattern2, '', content)

        # Match lines like: → Handoff templates: `reference/handoffs.md`
        pattern3 = rf'→[^\n]*`reference/{re.escape(basename)}`[^\n]*\n'
        content = re.sub(pattern3, '', content)

        # Match lines like: Handoff templates → `reference/handoff-formats.md`
        pattern4 = rf'[^\n]*→\s*`reference/{re.escape(basename)}`[^\n]*\n'
        content = re.sub(pattern4, '', content)

        # Match standalone reference lines
        pattern5 = rf'^[^\n|]*`reference/{re.escape(basename)}`[^\n]*$\n'
        content = re.sub(pattern5, '', content, flags=re.MULTILINE)

    # Clean up double blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original:
        with open(skill_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    # Step 1: Delete files
    deleted = delete_files()
    print(f"Deleted {len(deleted)} files")

    # Build list of deleted basenames for each agent
    all_deleted_basenames = set(DELETE_BASENAMES)

    # Step 2: Update SKILL.md files
    updated = []
    for skill_path in sorted(glob.glob(os.path.join(BASE, "*/SKILL.md"))):
        agent = os.path.basename(os.path.dirname(skill_path))

        # Determine which basenames to remove from this agent's SKILL.md
        basenames_to_remove = list(all_deleted_basenames)

        # Add Titan-specific deletions
        if agent == "titan":
            basenames_to_remove.extend([
                "guardrail-integration.md",
                "phase-context-scoring.md",
                "magi-protocol.md",
                "rally-coordination.md",
            ])

        if update_skill_references(skill_path, basenames_to_remove):
            updated.append(agent)

    print(f"Updated {len(updated)} SKILL.md files: {', '.join(updated)}")

    # Step 3: Report
    print(f"\nTotal files deleted: {len(deleted)}")
    print(f"Estimated lines removed: ~27,000+")

if __name__ == "__main__":
    main()
