import click
import os
from scribe.config import get_model_config
from scribe.plugins import get_plugin
from scribe.cli.utils import get_git_config_model
from scribe.cli.commit import commit
from scribe.cli.pr import pr
from scribe.cli.models import models
from scribe.cli.hooks.install import install
from scribe.cli.hooks.remove import remove
from scribe.cli.hooks.update import update
from scribe.cli.hooks.run import run


@click.group()
@click.option('--model', help='Specify the AI model to use')
@click.pass_context
def cli(ctx, model):
    ctx.ensure_object(dict)
    if model:
        os.environ['ZSCRIBE_MODEL'] = model
    else:
        git_config_model = get_git_config_model()
        if git_config_model:
            os.environ['ZSCRIBE_MODEL'] = git_config_model

    try:
        ctx.obj['config'] = get_model_config()
        ctx.obj['plugin'] = get_plugin(ctx.obj['config'])
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        ctx.abort()


@cli.command()
@click.pass_context
def commit_command(ctx):
    git_config_model = get_git_config_model('commit')
    if git_config_model:
        os.environ['ZSCRIBE_MODEL'] = git_config_model
    ctx.invoke(commit)


@cli.command()
@click.pass_context
def pr_command(ctx):
    git_config_model = get_git_config_model('pr')
    if git_config_model:
        os.environ['ZSCRIBE_MODEL'] = git_config_model
    ctx.invoke(pr)


cli.add_command(commit_command, name='commit')
cli.add_command(pr_command, name='pr')
cli.add_command(models)


@cli.group()
def hooks():
    """Manage git hooks."""
    pass


hooks.add_command(install)
hooks.add_command(remove)
hooks.add_command(update)
hooks.add_command(run)

if __name__ == '__main__':
    cli(obj={})