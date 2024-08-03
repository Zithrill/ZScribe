import argparse
import os
import sys
from git_utils import get_git_diff, parse_git_diff
from anthropic_api import generate_commit_message, refine_commit_message

def main():
    parser = argparse.ArgumentParser(description="Generate a commit message based on git diff.")
    parser.add_argument("commit1", help="The base commit hash")
    parser.add_argument("commit2", help="The compare commit hash")
    parser.add_argument("--refine", action="store_true", help="Refine the generated commit message")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
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