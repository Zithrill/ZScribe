import click
from scribe.cli.utils import get_git_hooks_dir, install_hook


@click.command()
@click.option(
    "--type",
    "hook_type",
    type=click.Choice(["commit", "pr", "both"]),
    default="both",
    help="Type of hook to install",
)
@click.option("--model", help="Specify the AI model to use for hooks")
def install(hook_type, model):
    """Install git hooks."""
    hooks_dir = get_git_hooks_dir()

    if hook_type in ["commit", "both"]:
        install_hook(
            hooks_dir, "prepare-commit-msg", "zscribe hooks run --type commit", model
        )
    if hook_type in ["pr", "both"]:
        install_hook(
            hooks_dir, "post-create-pull-request", "zscribe hooks run --type pr", model
        )

    click.echo(f"Installed {'both' if hook_type == 'both' else hook_type} hook(s).")
