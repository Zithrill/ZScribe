# src/scribe/pull_request_utils.py

import subprocess
from typing import List, Tuple


def get_pull_request_info(pr_number: str) -> Tuple[str, str, List[str]]:
    """
    Get information about a pull request.

    :param pr_number: The number of the pull request
    :return: A tuple containing (base_branch, head_branch, commit_messages)
    """
    # Get the base and head branches
    base_branch = subprocess.check_output(
        ['git', 'config', f'pullrequest.{pr_number}.base']
    ).decode().strip()
    head_branch = subprocess.check_output(
        ['git', 'config', f'pullrequest.{pr_number}.head']
    ).decode().strip()

    # Get the list of commits in the pull request
    commit_list = subprocess.check_output(
        ['git', 'log', f'{base_branch}..{head_branch}', '--pretty=format:%s']
    ).decode().strip().split('\n')

    return base_branch, head_branch, commit_list


def get_pull_request_diff(base_branch: str, head_branch: str) -> str:
    """
    Get the diff between the base and head branches of a pull request.

    :param base_branch: The base branch of the pull request
    :param head_branch: The head branch of the pull request
    :return: The diff between the two branches
    """
    diff = subprocess.check_output(
        ['git', 'diff', f'{base_branch}...{head_branch}']
    ).decode()

    return diff