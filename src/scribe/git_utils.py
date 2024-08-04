import subprocess
import re


def get_git_diff(commit1, commit2):
    try:
        result = subprocess.run(
            ["git", "diff", commit1, commit2],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        return None


def parse_git_diff(diff):
    files_changed = set()
    additions = 0
    deletions = 0
    file_pattern = re.compile(r'^\+\+\+ b/(.+)$')

    for line in diff.split('\n'):
        if line.startswith('+++'):
            match = file_pattern.match(line)
            if match:
                files_changed.add(match.group(1))
        elif line.startswith('+') and not line.startswith('+++'):
            additions += 1
        elif line.startswith('-') and not line.startswith('---'):
            deletions += 1

    summary = f"Files changed: {len(files_changed)}\n"
    summary += f"Additions: {additions}\n"
    summary += f"Deletions: {deletions}\n"
    summary += f"Modified files:\n"
    for file in sorted(files_changed):
        summary += f"  - {file}\n"

    return summary