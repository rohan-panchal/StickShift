import click

from shell import pass_context


@click.command('clear', short_help='Clears out a repo.')
@pass_context
def cli(ctx):

    if ctx.repository().clear():
        ctx.log("Migration Repository cleared")
    else:
        ctx.log("Migration Repository doesn't exist at that directory")
