#!/usr/bin/env python3
import os
import sys
import subprocess

def setup_git_hook():
    # Determine the Git hooks directory
    try:
        git_dir = subprocess.check_output(['git', 'rev-parse', '--git-dir']).decode('utf-8').strip()
        hooks_dir = os.path.join(git_dir, 'hooks')
    except subprocess.CalledProcessError:
        print("Error: Not a git repository. Please run this script from within a git repository.")
        sys.exit(1)

    # Path to the prepare-commit-msg hook
    hook_path = os.path.join(hooks_dir, 'prepare-commit-msg')

    # Content of the hook script
    hook_content = """#!/bin/sh
zithScribe-prepare-commit-msg "$1"
"""

    # Write the hook script
    with open(hook_path, 'w') as f:
        f.write(hook_content)

    # Make the hook executable
    os.chmod(hook_path, 0o755)

    print(f"Git hook installed successfully at {hook_path}")
    print("ZithScribe will now automatically generate commit messages when you run 'git commit'.")

if __name__ == "__main__":
    setup_git_hook()