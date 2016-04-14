import click

from shell import pass_context


@click.command('setup', short_help='Initializes a repo.')
@pass_context
def cli(ctx):

    if ctx.repository().create_repository():
        ctx.log("Migration Repository created")
    else:
        ctx.log("Migration Repository already setup")
