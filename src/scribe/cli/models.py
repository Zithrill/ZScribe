import click
from scribe.plugins import list_available_models


@click.command()
def models():
    """List all available models."""
    click.echo("Available models:")
    for provider, models in list_available_models().items():
        click.echo(f"\n{provider.capitalize()}:")
        for model in models:
            click.echo(f"  - {model}")