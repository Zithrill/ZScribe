import subprocess
from typing import List, Tuple
import click


def get_pull_request_info(pr_number: str) -> Tuple[str, str, List[str]]:
    """
    Get information about a pull request.

    :param pr_number: The number of the pull request
    :return: A tuple containing (base_branch, head_branch, commit_messages)
    """
    base_branch = "main"  # Default base branch
    head_branch = "unknown"  # Default head branch
    commit_messages = []  # Default empty list for commit messages

    try:
        # Try to get the base and head branches from git config
        base_branch = (
            subprocess.check_output(["git", "config", f"pullrequest.{pr_number}.base"])
            .decode()
            .strip()
        )
        head_branch = (
            subprocess.check_output(["git", "config", f"pullrequest.{pr_number}.head"])
            .decode()
            .strip()
        )
        click.echo(f"Got branches from git config: base={base_branch}, head={head_branch}")
    except subprocess.CalledProcessError:
        click.echo("Failed to get branches from git config, trying to get current branch")
        try:
            head_branch = (
                subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
                .decode()
                .strip()
            )
            click.echo(f"Got current branch: {head_branch}")
        except subprocess.CalledProcessError:
            click.echo("Failed to get current branch")

    # Get the list of commits in the pull request
    try:
        commit_list = (
            subprocess.check_output(
                ["git", "log", f"{base_branch}..{head_branch}", "--pretty=format:%s"]
            )
            .decode()
            .strip()
            .split("\n")
        )
        commit_messages = [msg for msg in commit_list if msg]  # Remove empty strings
        click.echo(f"Got {len(commit_messages)} commit messages")
    except subprocess.CalledProcessError:
        click.echo("Failed to get commit messages")

    click.echo(f"Returning: base={base_branch}, head={head_branch}, commits={len(commit_messages)}")
    return base_branch, head_branch, commit_messages


def get_pull_request_diff(base_branch: str, head_branch: str) -> str:
    """
    Get the diff between the base and head branches of a pull request.

    :param base_branch: The base branch of the pull request
    :param head_branch: The head branch of the pull request
    :return: The diff between the two branches
    """
    try:
        diff = subprocess.check_output(["git", "diff", f"{base_branch}...{head_branch}"]).decode()
    except subprocess.CalledProcessError:
        diff = ""

    return diff
