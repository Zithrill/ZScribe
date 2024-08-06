import subprocess
import re
from typing import Dict, List, Tuple


def get_git_diff(commit1, commit2):
    try:
        result = subprocess.run(
            ["git", "diff", commit1, commit2],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        return None


def determine_context_lines(hunk_lines: List[str]) -> int:
    """
    Determine the appropriate number of context lines based on the hunk content.
    Smaller changes get more context, larger changes get less.
    """
    total_lines = len(hunk_lines)
    changed_lines = sum(1 for line in hunk_lines if line.startswith(("+", "-")))
    unchanged_lines = total_lines - changed_lines

    if changed_lines <= 3:
        return min(unchanged_lines, 20)  # Max 20 lines for very small changes
    elif changed_lines <= 10:
        return min(unchanged_lines, 15)  # Max 15 lines for small changes
    elif changed_lines <= 25:
        return min(unchanged_lines // 2, 10)  # Max 10 lines for medium changes
    else:
        return min(unchanged_lines // 4, 5)  # Max 5 lines for large changes


def parse_git_diff(diff: str) -> str:
    files_changed: Dict[str, List[List[str]]] = {}
    current_file = ""
    hunk_changes: List[str] = []
    additions = 0
    deletions = 0
    file_pattern = re.compile(r"^(\+\+\+|\-\-\-) [ab]/(.+)$")
    hunk_pattern = re.compile(r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@")

    for line in diff.split("\n"):
        if line.startswith("+++"):
            match = file_pattern.match(line)
            if match:
                current_file = match.group(2)
                files_changed[current_file] = []
        elif hunk_pattern.match(line):
            if hunk_changes:
                files_changed[current_file].append(hunk_changes)
            hunk_changes = [line]
        else:
            hunk_changes.append(line)
            if line.startswith("+") and not line.startswith("+++"):
                additions += 1
            elif line.startswith("-") and not line.startswith("---"):
                deletions += 1

    if hunk_changes:
        files_changed[current_file].append(hunk_changes)

    summary = f"Files changed: {len(files_changed)}\n"
    summary += f"Additions: {additions}\n"
    summary += f"Deletions: {deletions}\n"
    summary += "Modified files with changes:\n\n"

    for file, hunks in files_changed.items():
        summary += f"File: {file}\n"
        summary += "=" * (len(file) + 6) + "\n\n"

        for hunk in hunks:
            if len(hunk) < 2:
                continue

            context_lines = determine_context_lines(hunk)
            context: List[str] = []
            changes: List[Tuple[str, List[str]]] = []

            for line in hunk[1:]:  # Skip the hunk header
                if line.startswith(("+", "-")):
                    if context:
                        changes.append(("context", context))
                        context = []
                    changes.append(("change", [line]))
                else:
                    context.append(line)
                    if len(context) > context_lines * 2:
                        context.pop(0)

            if context:
                changes.append(("context", context))

            for change_type, lines in changes:
                if change_type == "context":
                    summary += "  Context:\n"
                    for line in lines[:context_lines]:
                        summary += f"    {line}\n"
                    if len(lines) > context_lines:
                        summary += "    ...\n"
                        for line in lines[-context_lines:]:
                            summary += f"    {line}\n"
                else:
                    summary += "  Change:\n"
                    summary += f"    {lines}\n"

            summary += "\n"

        summary += "\n"

    return summary
