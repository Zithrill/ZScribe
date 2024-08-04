import click
from scribe.git_utils import get_git_diff, parse_git_diff


@click.command()
@click.argument('commit1')
@click.argument('commit2')
@click.option('--refine', is_flag=True, help='Refine the generated commit message')
@click.pass_context
def commit(ctx, commit1, commit2, refine):
    """Generate a commit message based on git diff."""
    diff = get_git_diff(commit1, commit2)
    if diff is None:
        click.echo("Error: Failed to get git diff.", err=True)
        ctx.abort()

    diff_summary = parse_git_diff(diff)

    try:
        commit_message = ctx.obj['plugin'].generate_commit_message(diff_summary)
        if refine:
            commit_message = ctx.obj['plugin'].refine_commit_message(commit_message, diff_summary)
        click.echo(f"Generated Commit Message (using {ctx.obj['config']['model']}):")
        click.echo(commit_message)
    except Exception as e:
        click.echo(f"Error generating commit message: {e}", err=True)
        ctx.abort()