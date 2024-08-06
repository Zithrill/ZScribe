import click
from scribe.cli.utils import update_hook_model


@click.command()
@click.option(
    "--type",
    "hook_type",
    type=click.Choice(["commit", "pr", "both"]),
    default="both",
    help="Type of hook to update",
)
@click.option("--model", required=True, help="Specify the new AI model to use for hooks")
def update(hook_type, model):
    """Update the AI model used by existing hooks."""
    update_hook_model(hook_type, model)
