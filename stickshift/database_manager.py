import psycopg2
from database_queries import create_table_drop_query,\
    query_function_drop_command, \
    QUERY_LIST_FUNCTIONS, \
    QUERY_LIST_TABLES, \
    QUERY_CREATE_MIGRATION_TABLE, \
    QUERY_DROP_MIGRATION_TABLE, \
    QUERY_DATABASE_MIGRATIONS_TABLE_EXISTS, \
    QUERY_DATABASE_CURRENT_VERSION, \
    QUERY_DATABASE_INSERT_MIGRATION, \
    QUERY_DATABASE_DELETE_MIGRATION, \
    QUERY_DATABASE_MIGRATION_VERSIONS


class DatabaseManager:

    def __init__(self, migration_repository, environment):
        self.migration_repository = migration_repository
        self.environment = environment
        self.database_config = migration_repository.database_config(self.environment)
        self.connection = None
        if self.database_config is not None:
            self.connection = psycopg2.connect(host=self.database_config["host"],
                                               port=self.database_config["port"],
                                               user=self.database_config["username"],
                                               password=self.database_config["password"],
                                               database=self.database_config["database"])
            self.connection.autocommit = True

    def provision_database(self):
        self.execute_create(QUERY_CREATE_MIGRATION_TABLE)
        print("Database provisioned")

    def deprovision_database(self):
        if self.is_database_provisioned():
            self.execute_create(QUERY_DROP_MIGRATION_TABLE)
            print("Database deprovisioned")
        else:
            print("Database is not provisioned")

    def is_database_provisioned(self):
        result = self.execute_fetch(QUERY_DATABASE_MIGRATIONS_TABLE_EXISTS)
        return result[0]

    def current_database_migration_version(self):
        result = self.execute_fetch(QUERY_DATABASE_CURRENT_VERSION)
        return result[0]

    def list_database_current_version(self):
        if self.is_database_provisioned():
            version = self.execute_fetch(QUERY_DATABASE_CURRENT_VERSION)
            print("Current Database Version:{0}".format(version[0]))
        else:
            print("Database is not provisioned")

    def list_migrations(self):
        migrations = self.migration_repository.current_migrations_list()
        print("\nMIGRATIONS")
        print("----------")
        for migration in migrations:
            print("{0}".format(migration))
        print("----------")

    def list_procedures(self):
        functions = self.execute_fetch(QUERY_LIST_FUNCTIONS)
        print("\nPROCEDURES")
        print("---------")
        for function in functions:
            print("{0}".format(function))
        print("---------")

    def list_tables(self):
        tables = self.execute_fetch(QUERY_LIST_TABLES)
        print("\nTABLES")
        print("------")
        for table in tables:
            print("{0}".format(table))
        print("---------\n")

    def execute_create(self, query=None):
        if query is not None:
            with self.connection.cursor() as cursor:
                cursor.execute(query)

    def execute_fetch(self, query=None):
        if query is not None:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                results = [row[0] for row in cursor]
                return results

    def migrate(self):
        migration_list = self.migration_repository.current_migrations_list()
        current_migration_version = self.current_database_migration_version()
        if current_migration_version is not None:
            migration_list = migration_list[(current_migration_version+1):]
        for idx, migration_file_name in enumerate(migration_list):
            self.execute_migration(migration_file_name=migration_file_name,
                                   version_index=self.find_migration_index(migration_file_name))

    def upgrade(self):
        migration_list = self.migration_repository.current_migrations_list()
        current_migration_version = self.current_database_migration_version()
        if current_migration_version is not None:
            migration_list = migration_list[(current_migration_version+1):]
        next_migration = migration_list[0]
        self.execute_migration(migration_file_name=next_migration,
                               version_index=self.find_migration_index(migration_file_name=next_migration))

    def reset(self, limit=0):
        downgrade_list = self.migration_repository.current_downgrade_list()
        current_migration_version = self.current_database_migration_version()
        limit = current_migration_version
        if current_migration_version is not None:
            downgrade_list = downgrade_list[0:limit+1]
        else:
            return
        downgrade_list.reverse()
        for idx, migration_file_name in enumerate(downgrade_list):
            self.execute_downgrade(migration_file_name=migration_file_name,
                                   version_index=self.find_migration_index(migration_file_name))

    def downgrade(self):
        downgrade_list = self.migration_repository.current_downgrade_list()
        current_migration_version = self.current_database_migration_version()
        limit = current_migration_version
        if current_migration_version is not None:
            downgrade_list = downgrade_list[0:limit+1]
        else:
            return
        downgrade_list.reverse()
        next_migration = downgrade_list[0]
        self.execute_downgrade(migration_file_name=next_migration,
                               version_index=self.find_migration_index(migration_file_name=next_migration))

    def find_migration_index(self, migration_file_name):
        underscore_index = migration_file_name.index("_")
        return migration_file_name[1:underscore_index]

    def execute_migration(self,
                          migration_file_name=None,
                          version_index=None):
        with self.connection.cursor() as cursor:
            cursor.execute(open(self.migration_repository.repository_upgrade_path() + "/" + migration_file_name, "r").read())
            cursor.execute(QUERY_DATABASE_INSERT_MIGRATION.format(version_index))
            print("Migration:{0} completed".format(migration_file_name))

    def execute_downgrade(self,
                          migration_file_name=None,
                          version_index=None):
        with self.connection.cursor() as cursor:
            cursor.execute(open(self.migration_repository.repository_downgrade_path() + "/" + migration_file_name, "r").read())
            cursor.execute(QUERY_DATABASE_DELETE_MIGRATION.format(version_index))
            print("Downgrade:{0} completed".format(migration_file_name))
