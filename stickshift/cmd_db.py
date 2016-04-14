import click

from shell import pass_context


@click.command('db', short_help='Run specific commands against a specific database')
@click.argument('operation', required=True, type=click.STRING, metavar='<operation>')
@click.argument('environment', required=True, type=click.STRING, metavar='<environment>')
@pass_context
def cli(ctx, operation, environment):

    if ctx.repository().is_repository_setup():

        database_manager = ctx.database_manager(environment=environment)

        if operation == "provision":
            database_manager.provision_database()
        elif operation == "deprovision":
            database_manager.deprovision_database()
        elif operation == "version":
            database_manager.list_database_current_version()
        elif operation == "versions":
            database_manager.list_database_versions()
        elif operation == "procedures":
            database_manager.list_procedures()
        elif operation == "tables":
            database_manager.list_tables()
        elif operation == "upgrade":
            database_manager.upgrade()
        elif operation == "downgrade":
            database_manager.downgrade()
        elif operation == "reset":
            database_manager.reset()

    else:
        print("Migration Repository must be setup before running database operations.")
