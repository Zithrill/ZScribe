import subprocess

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

        if not base_branch or not head_branch:
            click.echo(
                "Warning: Unable to determine base or head branch. Using current branch for comparison.",
                err=True,
            )
            base_branch = "main"  # Assume 'main' as the default base branch
            head_branch = (
                subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
                .decode()
                .strip()
            )

        diff = get_pull_request_diff(base_branch, head_branch)

        if not diff:
            click.echo(
                "Warning: No diff found between branches. The pull request might be empty or already merged.",
                err=True,
            )
            return

        diff_summary = parse_git_diff(diff)
        pr_message = ctx.obj["plugin"].generate_pull_request_message(diff_summary, commit_messages)

        click.echo(f"Generated Pull Request Description (using {ctx.obj['config']['model']}):")
        click.echo(pr_message)
    except Exception as e:
        click.echo(f"Error generating pull request description: {e}", err=True)
        click.echo("Please provide the following information manually:", err=True)
        click.echo("1. Base branch (e.g., 'main')", err=True)
        click.echo("2. Head branch (your current branch)", err=True)
        click.echo("3. A brief summary of your changes", err=True)
        ctx.abort()
