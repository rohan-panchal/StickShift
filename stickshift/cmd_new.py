import click

from shell import pass_context


@click.command('new', short_help='Creates a migration script for creating a new table or procedure')
@click.argument('type', required=True, type=click.STRING, metavar='<type>')
@click.argument('name', required=True, type=click.STRING, metavar='<name>')
@pass_context
def cli(ctx, type, name):

    if ctx.repository().is_repository_setup():
        if type == "table":
            ctx.repository().create_new_table_migration(name)
        elif type == "procedure":
            ctx.repository().create_new_procedure_migration(name)
    else:
        print("Migration Repository must be setup before creating migration scripts")
