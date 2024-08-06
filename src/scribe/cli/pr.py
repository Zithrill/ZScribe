import click
from scribe.pull_request_utils import get_pull_request_info, get_pull_request_diff
from scribe.git_utils import parse_git_diff


@click.command()
@click.argument("pr_number")
@click.pass_context
def pr(ctx, pr_number):
    """Generate a pull request description for the given PR number."""
    try:
        base_branch, head_branch, commit_messages = get_pull_request_info(pr_number)
        diff = get_pull_request_diff(base_branch, head_branch)
        diff_summary = parse_git_diff(diff)
        pr_message = ctx.obj["plugin"].generate_pull_request_message(diff_summary, commit_messages)
        click.echo(f"Generated Pull Request Description (using {ctx.obj['config']['model']}):")
        click.echo(pr_message)
    except Exception as e:
        click.echo(f"Error generating pull request description: {e}", err=True)
        ctx.abort()
