import unittest

from stickshift.migration_repository import MigrationRepository
from stickshift.database_manager import DatabaseManager


class DatabaseManagerTests(unittest.TestCase):

    def setUp(self):
        self.migration_repository = MigrationRepository()
        self.migration_repository.clear()
        self.migration_repository.create_repository()
        self.database_manager = DatabaseManager(migration_repository=self.migration_repository,
                                                environment="DATABASE")

    def tearDown(self):
        if self.database_manager.is_database_provisioned():
            self.database_manager.reset()
            self.database_manager.deprovision_database()
        self.migration_repository.clear()

    # Database Provisioning Tests

    def test_provision_database(self):
        self.database_manager.provision_database()
        assert(self.database_manager.is_database_provisioned())

    def test_deprovision_database(self):
        self.database_manager.provision_database()
        self.database_manager.deprovision_database()
        assert(self.database_manager.is_database_provisioned() == False)

    def test_deprovision_database_when_not_provisioned(self):
        assert(self.database_manager.is_database_provisioned() == False)
        self.database_manager.deprovision_database()
        assert(self.database_manager.is_database_provisioned() == False)

    # Database Versioning Tests

    def test_current_database_migration_version(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("users")
        self.database_manager.upgrade()
        assert(self.database_manager.current_database_migration_version() == 0)

    def test_current_database_migration_version_when_no_migrations(self):
        self.database_manager.provision_database()
        assert(self.database_manager.current_database_migration_version() is None)

    # Database Lists Tests

    def test_list_migrations(self):
        self.migration_repository.create_new_table_migration("users")
        assert(len(self.database_manager.list_migrations()) == 1)

    def test_list_procedures(self):
        # TODO: Redo the create_new_procedure_migration to accept a content field
        # TODO: so that i can run the migration without an error.
        pass

    def test_list_procedures_on_unprovisioned_database(self):
        assert(len(self.database_manager.list_procedures()) == 0)

    def test_list_tables(self):
        self.database_manager.provision_database()
        assert(len(self.database_manager.list_tables()) == 1)

    def test_list_tables_on_unprovisioned_database(self):
        assert(len(self.database_manager.list_tables()) == 0)

    # Database Migration Tests

    def test_migrate_runs_multiple_migrations(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("test_1")
        self.migration_repository.create_new_table_migration("test_2")
        assert(self.migration_repository.current_migration_count() == 2)
        assert(len(self.database_manager.list_tables()) == 1)
        self.database_manager.migrate()
        assert(len(self.database_manager.list_tables()) == 3)

    def test_migrate_runs_on_new_migrations(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("test_1")
        self.database_manager.upgrade()
        assert(len(self.database_manager.list_tables()) == 2)
        self.migration_repository.create_new_table_migration("test_2")
        self.database_manager.migrate()
        assert(len(self.database_manager.list_tables()) == 3)

    def test_upgrade_runs_only_one_migration(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("test_1")
        self.migration_repository.create_new_table_migration("test_2")
        assert(self.migration_repository.current_migration_count() == 2)
        assert(len(self.database_manager.list_tables()) == 1)
        self.database_manager.upgrade()
        assert(len(self.database_manager.list_tables()) == 2)

    def test_upgrade_runs_only_the_next_migration(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("test_1")
        self.migration_repository.create_new_table_migration("test_2")
        assert(self.migration_repository.current_migration_count() == 2)
        assert(len(self.database_manager.list_tables()) == 1)
        self.database_manager.upgrade()
        assert(len(self.database_manager.list_tables()) == 2)
        self.database_manager.upgrade()
        assert(len(self.database_manager.list_tables()) == 3)

    # Database Reset Tests

    def test_reset_runs_multiple_migrations(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("test_1")
        self.migration_repository.create_new_table_migration("test_2")
        assert(self.migration_repository.current_migration_count() == 2)
        assert(len(self.database_manager.list_tables()) == 1)
        self.database_manager.migrate()
        assert(len(self.database_manager.list_tables()) == 3)

        self.database_manager.reset()
        assert(len(self.database_manager.list_tables()) == 1)

    def test_reset_runs_on_remaining_migrations(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("test_1")
        self.migration_repository.create_new_table_migration("test_2")
        assert(self.migration_repository.current_migration_count() == 2)
        assert(len(self.database_manager.list_tables()) == 1)
        self.database_manager.migrate()
        assert(len(self.database_manager.list_tables()) == 3)

        self.database_manager.downgrade()
        assert(len(self.database_manager.list_tables()) == 2)

        self.database_manager.reset()
        assert(len(self.database_manager.list_tables()) == 1)

    def test_downgrade_runs_only_one_migration(self):
        self.database_manager.provision_database()
        self.migration_repository.create_new_table_migration("test_1")
        self.migration_repository.create_new_table_migration("test_2")
        assert(self.migration_repository.current_migration_count() == 2)
        assert(len(self.database_manager.list_tables()) == 1)
        self.database_manager.migrate()
        assert(len(self.database_manager.list_tables()) == 3)

        self.database_manager.downgrade()
        assert(len(self.database_manager.list_tables()) == 2)

    def test_downgrade_runs_only_when_there_is_a_current_version(self):
        self.database_manager.provision_database()
        assert(self.database_manager.downgrade() == False)
