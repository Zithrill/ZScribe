import sys
import os
import subprocess
from scribe.git_utils import parse_git_diff
from scribe.config import get_model_config
from scribe.plugins import get_plugin

def get_git_config_model():
    try:
        return subprocess.check_output(['git', 'config', 'zscribe.model']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def prepare_commit_msg(commit_msg_file):
    # Get the diff of staged changes
    diff = subprocess.check_output(['git', 'diff', '--cached']).decode('utf-8')

    if not diff:
        # No changes staged, exit without modifying the commit message
        return

    # Parse the diff using our new parse_git_diff function
    diff_summary = parse_git_diff(diff)

    try:
        # Get model from git config
        git_config_model = get_git_config_model()
        if git_config_model:
            os.environ['ZSCRIBE_MODEL'] = git_config_model

        # Get the model configuration
        config = get_model_config()
        # Get the appropriate plugin
        plugin = get_plugin(config)

        # Generate commit message
        commit_message = plugin.generate_commit_message(diff_summary)

        # Write the generated message to the commit message file
        with open(commit_msg_file, 'w') as f:
            f.write(f"# Generated by ZScribe using {config['model']}\n\n")
            f.write(commit_message)
            f.write("\n\n# Please review and edit the commit message as needed.\n")
            f.write("# Lines starting with '#' will be ignored.\n")

        print(f"Commit message generated using {config['model']}. Please review and edit if necessary.")

    except Exception as e:
        print(f"Error generating commit message: {e}")
        print("Please write your commit message manually.")
        # In case of error, we don't modify the commit message file
        return

if __name__ == "__main__":
    prepare_commit_msg(sys.argv[1])