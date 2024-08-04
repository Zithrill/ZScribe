import click


@click.command()
@click.option('--type', 'hook_type', type=click.Choice(['commit', 'pr']), required=True, help='Type of hook to run')
@click.argument('args', nargs=-1)
@click.pass_context
def run(ctx, hook_type, args):
    """Run git hooks (internal use)."""
    if hook_type == 'commit':
        from scribe.prepare_commit_msg import prepare_commit_msg
        prepare_commit_msg(args[0])
    elif hook_type == 'pr':
        from scribe.pr_hook_script import generate_pr_description
        generate_pr_description(args[0])