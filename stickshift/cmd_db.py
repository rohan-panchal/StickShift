import click

from shell import pass_context

DB_OPERATIONS = [
    "provision",
    "deprovision",
    "version",
    "procedures",
    "tables",
    "migrate",
    "reset",
    "upgrade",
    "downgrade",
]


@click.command('db', short_help='Run specific commands against a specific database')
@click.argument('operation', required=True, type=click.Choice(DB_OPERATIONS), metavar='<operation>')
@click.argument('environment', required=True, type=click.STRING, metavar='<environment>')
@pass_context
def cli(ctx, operation, environment):

    if ctx.repository().is_repository_setup():
        database_manager = ctx.database_manager(environment=environment)
        if operation == "provision":
            provision_database(database_manager=database_manager)
        elif operation == "deprovision":
            database_manager.deprovision_database(database_manager=database_manager)
        elif operation == "version":
            print_database_version(database_manager=database_manager)
        elif operation == "procedures":
            print_list_items_with_title(title="PROCEDURES", list_items=database_manager.list_procedures())
        elif operation == "tables":
            print_list_items_with_title(title="TABLES", list_items=database_manager.list_tables())
        elif operation == "upgrade":
            database_manager.upgrade()
        elif operation == "downgrade":
            database_manager.downgrade()
        elif operation == "migrate":
            database_manager.migrate()
        elif operation == "reset":
            database_manager.reset()

    else:
        print("Migration Repository must be setup before running database operations.")


def provision_database(database_manager):
    if database_manager.provision_database():
        print("Database provisioned successfully")
    else:
        print("Database is already provisioned")


def deprovision_database(database_manager):
    if database_manager.deprovision_database():
        print("Database deprovisioned successfully")
    else:
        print("Database is not provisioned")


def print_database_version(database_manager):
    version = database_manager.current_database_migration_version()
    if version is not None:
        print("Version: {0}".format(version))
    else:
        print("Database is not provisioned")


def print_list_items_with_title(title, list_items):
    print("\n{0}".format(title))
    print("--------")
    for item in list_items:
        print(item)
    print("--------")
