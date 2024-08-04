#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse


def get_git_hooks_dir():
    try:
        git_dir = subprocess.check_output(['git', 'rev-parse', '--git-dir']).decode('utf-8').strip()
        return os.path.join(git_dir, 'hooks')
    except subprocess.CalledProcessError:
        print("Error: Not a git repository. Please run this script from within a git repository.")
        sys.exit(1)


def install_hook(hooks_dir, hook_name, script_name):
    hook_path = os.path.join(hooks_dir, hook_name)
    hook_content = f"""#!/bin/sh
{script_name} "$@"
"""
    with open(hook_path, 'w') as f:
        f.write(hook_content)
    os.chmod(hook_path, 0o755)
    print(f"Installed {hook_name} hook.")


def remove_hook(hooks_dir, hook_name):
    hook_path = os.path.join(hooks_dir, hook_name)
    if os.path.exists(hook_path):
        os.remove(hook_path)
        print(f"Removed {hook_name} hook.")
    else:
        print(f"{hook_name} hook not found.")


def setup_git_hooks():
    parser = argparse.ArgumentParser(description="Install or remove ZithScribe git hooks.")
    parser.add_argument('--install', choices=['commit', 'pr', 'both'], help="Install specified hook(s)")
    parser.add_argument('--remove', choices=['commit', 'pr', 'both'], help="Remove specified hook(s)")
    args = parser.parse_args()

    hooks_dir = get_git_hooks_dir()

    if args.install:
        if args.install in ['commit', 'both']:
            install_hook(hooks_dir, 'prepare-commit-msg', 'zithScribe-prepare-commit-msg')
        if args.install in ['pr', 'both']:
            install_hook(hooks_dir, 'post-create-pull-request', 'zithScribe-pr-hook')
    elif args.remove:
        if args.remove in ['commit', 'both']:
            remove_hook(hooks_dir, 'prepare-commit-msg')
        if args.remove in ['pr', 'both']:
            remove_hook(hooks_dir, 'post-create-pull-request')
    else:
        # Default behavior: install both hooks
        install_hook(hooks_dir, 'prepare-commit-msg', 'zithScribe-prepare-commit-msg')
        install_hook(hooks_dir, 'post-create-pull-request', 'zithScribe-pr-hook')
        print("Installed both commit message and pull request hooks by default.")


if __name__ == "__main__":
    setup_git_hooks()
