from unittest.mock import patch
import subprocess
from scribe.pull_request_utils import get_pull_request_info, get_pull_request_diff


def test_get_pull_request_info(mocker):
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_check_output.side_effect = [b"main\n", b"feature-branch\n", b"Commit 1\nCommit 2\n"]
    base_branch, head_branch, commit_messages = get_pull_request_info("123")
    assert base_branch == "main"
    assert head_branch == "feature-branch"
    assert commit_messages == ["Commit 1", "Commit 2"]


def test_get_pull_request_info_all_error(mocker):
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")

    base_branch, head_branch, commit_messages = get_pull_request_info("123")
    assert base_branch == "main"
    assert head_branch == "unknown"
    assert commit_messages == []


def test_get_pull_request_diff(mocker):
    mock_check_output = mocker.patch("subprocess.check_output")
    mock_diff = b"diff --git a/file.py b/file.py\n..."
    mock_check_output.return_value = mock_diff
    diff = get_pull_request_diff("main", "feature-branch")
    assert diff == mock_diff.decode()


@patch("subprocess.check_output")
def test_get_pull_request_diff_error(mock_check_output):
    mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")
    diff = get_pull_request_diff("main", "feature-branch")
    assert diff == ""
