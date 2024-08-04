import unittest
from unittest.mock import patch, MagicMock
from scribe.git_utils import get_git_diff, parse_git_diff
from scribe.anthropic_api import generate_commit_message, refine_commit_message
from scribe.main import main


class TestAutoDescribe(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_git_diff(self, mock_run):
        mock_run.return_value = MagicMock(stdout="mock diff output")
        diff = get_git_diff("commit1", "commit2")
        self.assertEqual(diff, "mock diff output")
        mock_run.assert_called_once_with(
            ["git", "diff", "commit1", "commit2"],
            capture_output=True,
            text=True,
            check=True
        )

    def test_parse_git_diff(self):
        mock_diff = """diff --git a/file1.py b/file1.py
index 1234567..abcdefg 100644
--- a/file1.py
+++ b/file1.py
@@ -1,5 +1,6 @@
 def hello():
-    print("Hello, World!")
+    print("Hello, Universe!")
+    print("Welcome!")

 def goodbye():
     print("Goodbye!")
diff --git a/file2.py b/file2.py
index 2345678..bcdefgh 100644
--- a/file2.py
+++ b/file2.py
@@ -1,3 +1,4 @@
 def add(a, b):
     return a + b
+
+def subtract(a, b):
+    return a - b"""

        result = parse_git_diff(mock_diff)
        expected = """Files changed: 2
Additions: 3
Deletions: 1
Modified files:
  - file1.py
  - file2.py
"""
        self.assertEqual(result, expected)

    @patch('anthropic.Anthropic')
    def test_generate_commit_message(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.completions.create.return_value = MagicMock(completion="Mock commit message")

        message = generate_commit_message("Mock diff summary")
        self.assertEqual(message, "Mock commit message")
        mock_client.completions.create.assert_called_once()

    @patch('anthropic.Anthropic')
    def test_refine_commit_message(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.completions.create.return_value = MagicMock(completion="Refined mock commit message")

        message = refine_commit_message("Original message", "Mock diff summary")
        self.assertEqual(message, "Refined mock commit message")
        mock_client.completions.create.assert_called_once()

    @patch('scribe.main.get_git_diff')
    @patch('scribe.main.parse_git_diff')
    @patch('scribe.main.generate_commit_message')
    @patch('scribe.main.refine_commit_message')
    def test_main(self, mock_refine, mock_generate, mock_parse, mock_get_diff):
        mock_get_diff.return_value = "mock diff"
        mock_parse.return_value = "mock summary"
        mock_generate.return_value = "mock message"
        mock_refine.return_value = "refined mock message"

        with patch('sys.argv', ['git-commit-message-generator', 'commit1', 'commit2']):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_with("mock message")

        with patch('sys.argv', ['git-commit-message-generator', 'commit1', 'commit2', '--refine']):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_with("refined mock message")


if __name__ == '__main__':
    unittest.main()