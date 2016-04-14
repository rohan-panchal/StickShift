import click

from shell import ShellCLI, pass_context

CONTEXT_SETTINGS = dict(auto_envvar_prefix='STICKSHIFT')


@click.command(cls=ShellCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--directory', type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help='Sets the root directory that should hold the Migration Repository.')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def cli(ctx, directory, verbose):
    ctx.directory = directory
    ctx.verbose = verbose
