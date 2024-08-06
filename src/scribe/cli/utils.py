import os
import subprocess
import click


def get_git_config_model(hook_type=None):
    try:
        if hook_type == "commit":
            return (
                subprocess.check_output(["git", "config", "zscribe.model.commit"])
                .decode("utf-8")
                .strip()
            )
        elif hook_type == "pr":
            return (
                subprocess.check_output(["git", "config", "zscribe.model.pr"])
                .decode("utf-8")
                .strip()
            )
        else:
            return (
                subprocess.check_output(["git", "config", "zscribe.model"]).decode("utf-8").strip()
            )
    except subprocess.CalledProcessError:
        return None


def get_git_hooks_dir():
    try:
        git_dir = subprocess.check_output(["git", "rev-parse", "--git-dir"]).decode("utf-8").strip()
        return os.path.join(git_dir, "hooks")
    except subprocess.CalledProcessError:
        raise ValueError(
            "Not a git repository. Please run this command from within a git repository."
        )


def install_hook(hooks_dir, hook_name, script_name, model=None):
    hook_path = os.path.join(hooks_dir, hook_name)
    hook_content = f"""#!/bin/sh
{script_name} "$@"
"""
    with open(hook_path, "w") as f:
        f.write(hook_content)
    os.chmod(hook_path, 0o755)
    click.echo(f"Installed {hook_name} hook.")

    if model:
        if hook_name == "prepare-commit-msg":
            subprocess.run(["git", "config", "zscribe.model.commit", model])
            click.echo(f"Set ZScribe commit hook model to {model} in git config.")
        elif hook_name == "post-create-pull-request":
            subprocess.run(["git", "config", "zscribe.model.pr", model])
            click.echo(f"Set ZScribe PR hook model to {model} in git config.")
        subprocess.run(["git", "config", "zscribe.model", model])
        click.echo(f"Set global ZScribe model to {model} in git config.")


def remove_hook(hooks_dir, hook_name):
    hook_path = os.path.join(hooks_dir, hook_name)
    if os.path.exists(hook_path):
        os.remove(hook_path)
        click.echo(f"Removed {hook_name} hook.")
    else:
        click.echo(f"{hook_name} hook not found.")


def update_hook_model(hook_type, model):
    if not model:
        click.echo("Error: Please specify a model to update to.", err=True)
        raise click.Abort()

    try:
        if hook_type in ["commit", "both"]:
            subprocess.run(["git", "config", "zscribe.model.commit", model], check=True)
            click.echo(f"Updated ZScribe commit hook model to {model} in git config.")

        if hook_type in ["pr", "both"]:
            subprocess.run(["git", "config", "zscribe.model.pr", model], check=True)
            click.echo(f"Updated ZScribe PR hook model to {model} in git config.")

        if hook_type == "both":
            subprocess.run(["git", "config", "zscribe.model", model], check=True)
            click.echo(f"Updated global ZScribe model to {model} in git config.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error updating git config: {e}", err=True)
        raise click.Abort()
