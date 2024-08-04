# src/scribe/main.py

import argparse
import os
import sys
from scribe.git_utils import get_git_diff, parse_git_diff
from scribe.pull_request_utils import get_pull_request_info, get_pull_request_diff
from scribe.config import get_model_config, MODEL_PROVIDER_MAP
from scribe.plugins import get_plugin, list_available_models

def main():
    parser = argparse.ArgumentParser(description="Generate a commit message or pull request description based on git diff.")
    parser.add_argument("--pr", help="Generate a pull request description for the given PR number")
    parser.add_argument("commit1", nargs="?", help="The base commit hash")
    parser.add_argument("commit2", nargs="?", help="The compare commit hash")
    parser.add_argument("--refine", action="store_true", help="Refine the generated commit message")
    parser.add_argument("--model", choices=list(MODEL_PROVIDER_MAP.keys()), help="Specify the AI model to use")
    parser.add_argument("--list-models", action="store_true", help="List all available models")
    args = parser.parse_args()

    if args.list_models:
        print("Available models:")
        print(list_available_models())
        for provider, models in list_available_models().items():
            print(f"\n{provider.capitalize()}:")
            for model in models:
                print(f"  - {model}")
        sys.exit(0)

    if args.model:
        os.environ['ZSCRIBE_MODEL'] = args.model

    try:
        config = get_model_config()
        plugin = get_plugin(config)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    if args.pr:
        # Handle pull request description generation
        try:
            base_branch, head_branch, commit_messages = get_pull_request_info(args.pr)
            diff = get_pull_request_diff(base_branch, head_branch)
            diff_summary = parse_git_diff(diff)
            pr_message = plugin.generate_pull_request_message(diff_summary, commit_messages)
            print(f"Generated Pull Request Description (using {config['model']}):")
            print(pr_message)
        except Exception as e:
            print(f"Error generating pull request description: {e}")
            sys.exit(1)
    else:
        # Commit message generation logic
        if not args.commit1 or not args.commit2:
            print("Error: Both commit1 and commit2 are required when not generating a pull request description.")
            sys.exit(1)

        # Get the git diff
        diff = get_git_diff(args.commit1, args.commit2)
        if diff is None:
            print("Error: Failed to get git diff.")
            sys.exit(1)

        # Parse the diff
        diff_summary = parse_git_diff(diff)

        # Generate commit message using the selected plugin
        try:
            commit_message = plugin.generate_commit_message(diff_summary)
            if args.refine:
                commit_message = plugin.refine_commit_message(commit_message, diff_summary)
            print(f"Generated Commit Message (using {config['model']}):")
            print(commit_message)
        except Exception as e:
            print(f"Error generating commit message: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()