import unittest

from stickshift.migration_repository import MigrationRepository


class MigratinRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.migration_repository = MigrationRepository()

    def test_migration_repository_create(self):
        self.migration_repository.clear()
        self.migration_repository.create_repository()
        assert(self.migration_repository.is_repository_setup() == True)

    def test_migration_repository_create_fail(self):
        self.migration_repository.clear()
        self.migration_repository.create_repository()
        assert(self.migration_repository.create_repository() == False)

    def test_migration_repository_clear_false(self):
        self.migration_repository.clear()
        assert(self.migration_repository.clear() == False)

    def test_migration_repository_is_setup(self):
        self.migration_repository.clear()
        assert(self.migration_repository.is_repository_setup() == False)
        self.migration_repository.create_repository()
        assert(self.migration_repository.is_repository_setup() == True)

    def test_table_creation_migration(self):
        self.migration_repository.clear()

        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_migrations_list() == ["V00__create_table_test.sql"])

    def test_table_alteration_migration(self):
        self.migration_repository.clear()

        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_alteration_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_migrations_list() == ["V00__alter_table_test.sql"])

    def test_procedure_creation_migration(self):
        self.migration_repository.clear()

        self.migration_repository.create_repository()
        self.migration_repository.create_new_procedure_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_migrations_list() == ["V00__create_sp_test.sql"])

    def test_migration_count(self):
        self.migration_repository.clear()

        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_downgrade_count() == 1)

    def test_migration_list(self):
        self.migration_repository.clear()

        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_migration("test")
        print(self.migration_repository.current_migrations_list())
        assert(self.migration_repository.current_migrations_list() == ["V00__create_table_test.sql"])

    def test_database_config(self):
        self.migration_repository.clear()

        self.migration_repository.create_repository()
        config = self.migration_repository.database_config("DATABASE")
        assert(config == {
            "host": "DB_HOST",
            "port": "DB_PORT",
            "username": "DB_USERNAME",
            "password": "DB_PASSWORD",
            "database": "DB_NAME"})
