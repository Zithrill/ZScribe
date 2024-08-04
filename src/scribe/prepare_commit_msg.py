#!/usr/bin/env python3
import sys
import os
import subprocess
from scribe.git_utils import get_git_diff, parse_git_diff
from scribe.anthropic_api import generate_commit_message


def main():
    # The commit message file is passed as the first argument
    commit_msg_file = sys.argv[1]

    # Get the diff of staged changes
    diff = subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')

    if not diff:
        # No changes staged, exit without modifying the commit message
        return

    # Parse the diff
    diff_summary = parse_git_diff(diff)

    # Generate commit message
    commit_message = generate_commit_message(diff_summary)

    # Write the generated message to the commit message file
    with open(commit_msg_file, 'w') as f:
        f.write(commit_message)


if __name__ == "__main__":
    main()