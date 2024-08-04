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


def setup_model_config(ctx, model, hook_type=None):
    if model:
        os.environ['ZSCRIBE_MODEL'] = model
    else:
        git_config_model = get_git_config_model(hook_type)
        if git_config_model:
            os.environ['ZSCRIBE_MODEL'] = git_config_model

    try:
        ctx.obj['config'] = get_model_config()
        ctx.obj['plugin'] = get_plugin(ctx.obj['config'])
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        ctx.abort()


@click.group()
@click.option('--model', help='Specify the AI model to use')
@click.pass_context
def cli(ctx, model):
    """ZScribe CLI for generating commit messages and PR descriptions."""
    ctx.ensure_object(dict)
    setup_model_config(ctx, model)


@cli.command()
@click.argument('commit1')
@click.argument('commit2')
@click.option('--refine', is_flag=True, help='Refine the generated commit message')
@click.pass_context
def commit_command(ctx, commit1, commit2, refine):
    """Generate a commit message."""
    git_config_model = get_git_config_model('commit')
    if git_config_model:
        os.environ['ZSCRIBE_MODEL'] = git_config_model
    setup_model_config(ctx, None, 'commit')
    ctx.invoke(commit, commit1=commit1, commit2=commit2, refine=refine)


@cli.command()
@click.argument('pr_number')
@click.pass_context
def pr_command(ctx, pr_number):
    """Generate a pull request description."""
    git_config_model = get_git_config_model('pr')
    if git_config_model:
        os.environ['ZSCRIBE_MODEL'] = git_config_model
    setup_model_config(ctx, None, 'pr')
    ctx.invoke(pr, pr_number=pr_number)


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