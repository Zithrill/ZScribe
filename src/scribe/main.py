import argparse
import os
import sys
from scribe.git_utils import get_git_diff, parse_git_diff
from scribe.anthropic_api import generate_commit_message, refine_commit_message, generate_pull_request_message
from scribe.pull_request_utils import get_pull_request_info, get_pull_request_diff

def main():
    parser = argparse.ArgumentParser(description="Generate a commit message or pull request description based on git diff.")
    parser.add_argument("--pr", help="Generate a pull request description for the given PR number")
    parser.add_argument("commit1", nargs="?", help="The base commit hash")
    parser.add_argument("commit2", nargs="?", help="The compare commit hash")
    parser.add_argument("--refine", action="store_true", help="Refine the generated commit message")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        sys.exit(1)

    if args.pr:
        # Handle pull request description generation
        try:
            base_branch, head_branch, commit_messages = get_pull_request_info(args.pr)
            diff = get_pull_request_diff(base_branch, head_branch)
            diff_summary = parse_git_diff(diff)
            pr_message = generate_pull_request_message(diff_summary, commit_messages)
            print("Generated Pull Request Description:")
            print(pr_message)
        except Exception as e:
            print(f"Error generating pull request description: {e}")
            sys.exit(1)
    else:
        # Existing commit message generation logic
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

        # Generate commit message using Anthropic API
        try:
            commit_message = generate_commit_message(diff_summary)
            if args.refine:
                commit_message = refine_commit_message(commit_message, diff_summary)
        except Exception as e:
            print(f"Error generating commit message: {e}")
            sys.exit(1)

        # Print the generated commit message
        print("Generated Commit Message:")
        print(commit_message)

if __name__ == "__main__":
    main()