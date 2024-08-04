import subprocess

import pytest
from unittest.mock import patch, MagicMock
from scribe.pull_request_utils import get_pull_request_info, get_pull_request_diff


@patch("subprocess.check_output")
def test_get_pull_request_info(mock_check_output):
    mock_check_output.side_effect = [
        b"main\n",
        b"feature-branch\n",
        b"Commit 1\nCommit 2\n",
    ]

    base_branch, head_branch, commit_messages = get_pull_request_info("123")

    assert base_branch == "main"
    assert head_branch == "feature-branch"
    assert commit_messages == ["Commit 1", "Commit 2"]

    assert mock_check_output.call_count == 3
    mock_check_output.assert_any_call(["git", "config", "pullrequest.123.base"])
    mock_check_output.assert_any_call(["git", "config", "pullrequest.123.head"])
    mock_check_output.assert_any_call(
        ["git", "log", "main..feature-branch", "--pretty=format:%s"]
    )


@patch("subprocess.check_output")
def test_get_pull_request_diff(mock_check_output):
    mock_diff = b"diff --git a/file.py b/file.py\n..."
    mock_check_output.return_value = mock_diff

    diff = get_pull_request_diff("main", "feature-branch")

    assert diff == mock_diff.decode()
    mock_check_output.assert_called_once_with(["git", "diff", "main...feature-branch"])


@patch("subprocess.check_output")
def test_get_pull_request_info_error(mock_check_output):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")

    with pytest.raises(subprocess.CalledProcessError):
        get_pull_request_info("123")


@patch("subprocess.check_output")
def test_get_pull_request_diff_error(mock_check_output):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")

    with pytest.raises(subprocess.CalledProcessError):
        get_pull_request_diff("main", "feature-branch")
