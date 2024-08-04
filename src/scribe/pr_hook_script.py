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
    prepare_commit_msg_path = os.path.join(hooks_dir, 'prepare-commit-msg')

    # Content of the prepare-commit-msg hook script
    prepare_commit_msg_content = """#!/bin/sh
zithScribe-prepare-commit-msg "$1"
"""

    # Write the prepare-commit-msg hook script
    with open(prepare_commit_msg_path, 'w') as f:
        f.write(prepare_commit_msg_content)

    # Make the prepare-commit-msg hook executable
    os.chmod(prepare_commit_msg_path, 0o755)

    # Path to the post-create-pull-request hook
    post_create_pr_path = os.path.join(hooks_dir, 'post-create-pull-request')

    # Content of the post-create-pull-request hook script
    post_create_pr_content = """#!/bin/sh
zithScribe-pr-hook "$1"
"""

    # Write the post-create-pull-request hook script
    with open(post_create_pr_path, 'w') as f:
        f.write(post_create_pr_content)

    # Make the post-create-pull-request hook executable
    os.chmod(post_create_pr_path, 0o755)

    print(f"Git hooks installed successfully at {hooks_dir}")
    print("ZithScribe will now automatically generate commit messages when you run 'git commit'")
    print("and pull request descriptions when you run 'git pull-request'.")

if __name__ == "__main__":
    setup_git_hook()