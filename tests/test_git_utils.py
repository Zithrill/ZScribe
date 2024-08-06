import pytest
from scribe.git_utils import get_git_diff, parse_git_diff


@pytest.fixture
def sample_diff():
    return """
diff --git a/file1.py b/file1.py
index 1234567..890abcd 100644
--- a/file1.py
+++ b/file1.py
@@ -1,3 +1,4 @@
 def hello():
-    print("Hello")
+    print("Hello, World!")
+    return True
diff --git a/file2.py b/file2.py
index 2345678..901bcde 100644
--- a/file2.py
+++ b/file2.py
@@ -1,2 +1,3 @@
 def goodbye():
     print("Goodbye")
+    return False
"""


def test_get_git_diff(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.stdout = "Mock diff output"
    mock_run.return_value.returncode = 0

    result = get_git_diff("commit1", "commit2")
    assert result == "Mock diff output"

    mock_run.assert_called_once_with(
        ["git", "diff", "commit1", "commit2"],
        capture_output=True,
        text=True,
        check=True,
    )


def test_parse_git_diff(sample_diff):
    summary = parse_git_diff(sample_diff)

    # Check the summary statistics
    assert "Files changed: 2" in summary
    assert "Additions: 3" in summary
    assert "Deletions: 1" in summary
    assert "Modified files with changes:" in summary

    # Check for the presence of both modified files
    assert "File: file1.py" in summary
    assert "File: file2.py" in summary

    # Check for the presence of context and change sections
    assert "  Context:" in summary
    assert "  Change:" in summary

    # Check for specific changes in file1.py
    assert '-    print("Hello")' in summary
    assert '+    print("Hello, World!")' in summary
    assert "+    return True" in summary

    # Check for specific changes in file2.py
    assert "+    return False" in summary

    # Check for the formatting of file sections
    assert "=" * 12 in summary  # Length of "File: file1.py" + 6

    # Optionally, you can add more specific checks based on the exact formatting you expect
