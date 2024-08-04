import click
from scribe.cli.utils import get_git_hooks_dir, remove_hook


@click.command()
@click.option(
    "--type",
    "hook_type",
    type=click.Choice(["commit", "pr", "both"]),
    default="both",
    help="Type of hook to remove",
)
def remove(hook_type):
    """Remove git hooks."""
    hooks_dir = get_git_hooks_dir()

    if hook_type in ["commit", "both"]:
        remove_hook(hooks_dir, "prepare-commit-msg")
    if hook_type in ["pr", "both"]:
        remove_hook(hooks_dir, "post-create-pull-request")

    click.echo(f"Removed {'both' if hook_type == 'both' else hook_type} hook(s).")
