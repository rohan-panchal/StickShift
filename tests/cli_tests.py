import unittest

from click.testing import CliRunner

from stickshift.migration_repository import MigrationRepository
from stickshift.database_manager import DatabaseManager

from stickshift.cli import cli
from stickshift.cli_strings import CLIStrings


class CLITests(unittest.TestCase):

    def setUp(self):
        self.migration_repository = MigrationRepository()
        self.migration_repository.clear()
        self.runner = CliRunner()

    def tearDown(self):
        self.migration_repository.clear()

    def test_cli(self):
        result = self.runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

    def test_cli_setup(self):
        result = self.runner.invoke(cli, ["setup"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(CLIStrings.DB_MIGRATION_REPOSITORY_CREATED == result.output.rstrip(), "output incorrect")

    def test_cli_setup_after_already_setup(self):
        result = self.runner.invoke(cli, ["setup"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_MIGRATION_REPOSITORY_CREATED, "output incorrect")
        result = self.runner.invoke(cli, ["setup"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_MIGRATION_REPOSITORY_ALREADY_CREATED, "output incorrect")

    def test_cli_clear_after_setup(self):
        result = self.runner.invoke(cli, ["setup"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(cli, ["clear"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_MIGRATION_REPOSITORY_CLEARED, "output incorrect")

    def test_cli_clear_after_already_cleared(self):
        result = self.runner.invoke(cli, ["setup"])
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(cli, ["clear"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_MIGRATION_REPOSITORY_CLEARED, "output incorrect")

    def test_cli_database_command_when_not_setup(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_MIGRATION_REPOSITORY_MUST_BE_SETUP)

    def test_cli_clear_when_not_setup(self):
        result = self.runner.invoke(cli, ["clear"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_MIGRATION_REPOSITORY_DOESNT_EXIST_AT_DIRECTORY)

    def test_cli_new_when_not_setup(self):
        result = self.runner.invoke(cli, ["new", "table", "test"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_MIGRATION_REPOSITORY_MUST_BE_SETUP)


class CLIDatabaseTests(unittest.TestCase):

    def setUp(self):
        self.migration_repository = MigrationRepository()
        self.migration_repository.clear()
        self.migration_repository.create_repository()
        self.database_manager = DatabaseManager(migration_repository=self.migration_repository,
                                                environment="DATABASE")
        self.runner = CliRunner()

    def tearDown(self):
        if self.database_manager.is_database_provisioned():
            self.database_manager.reset()
            self.database_manager.deprovision_database()
        self.migration_repository.clear()

    def test_cli_provision_database(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_DATABASE_PROVISIONED_SUCCESSFULLY)
        self.assertTrue(self.database_manager.is_database_provisioned())

    def test_cli_deprovision_database(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_DATABASE_PROVISIONED_SUCCESSFULLY)
        self.assertTrue(self.database_manager.is_database_provisioned())

        result = self.runner.invoke(cli, ["db", "deprovision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_DATABASE_DEPROVISIONED_SUCCESSFULLY)
        self.assertFalse(self.database_manager.is_database_provisioned())

    def test_cli_provision_when_already_provisioned(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_DATABASE_PROVISIONED_SUCCESSFULLY)
        self.assertTrue(self.database_manager.is_database_provisioned())

        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_DATABASE_IS_ALREADY_PROVISIONED)
        self.assertTrue(self.database_manager.is_database_provisioned())

    def test_cli_deprovision_when_not_provisioned(self):
        result = self.runner.invoke(cli, ["db", "deprovision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_DATABASE_IS_NOT_PROVISIONED)
        self.assertFalse(self.database_manager.is_database_provisioned())

    def test_cli_version_non_migrated(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["db", "version", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), CLIStrings.DB_DATABASE_NOT_MIGRATED_YET)

    def test_cli_version_migrated(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)

        self.runner.invoke(cli, ["new", "table", "test"])
        self.runner.invoke(cli, ["db", "migrate", "DATABASE"])

        result = self.runner.invoke(cli, ["db", "version", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), "{0}: {1}".format(CLIStrings.DB_DATABASE_VERSION, 0))

    def test_cli_list_tables(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(cli, ["db", "tables", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), "\nTABLES\n--------\nversion_migration\n--------")

    def test_cli_list_procedures(self):
        result = self.runner.invoke(cli, ["db", "procedures", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.rstrip(), "\nPROCEDURES\n--------\n--------")

    def test_cli_upgrade(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)

        self.runner.invoke(cli, ["new", "table", "test"])
        self.runner.invoke(cli, ["db", "upgrade", "DATABASE"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.database_manager.current_database_migration_version(), 0)

    def test_cli_downgrade(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)

        self.runner.invoke(cli, ["new", "table", "test"])
        self.runner.invoke(cli, ["db", "upgrade", "DATABASE"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.database_manager.current_database_migration_version(), 0)

        result = self.runner.invoke(cli, ["db", "downgrade", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.database_manager.current_database_migration_version(), None)

    def test_cli_migrate(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)

        self.runner.invoke(cli, ["new", "table", "test"])
        self.runner.invoke(cli, ["db", "upgrade", "DATABASE"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.database_manager.current_database_migration_version(), 0)

    def test_cli_reset(self):
        result = self.runner.invoke(cli, ["db", "provision", "DATABASE"])
        self.assertEqual(result.exit_code, 0)

        self.runner.invoke(cli, ["new", "table", "test"])
        self.runner.invoke(cli, ["db", "migrate", "DATABASE"])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.database_manager.current_database_migration_version(), 0)

        result = self.runner.invoke(cli, ["db", "reset", "DATABASE"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(self.database_manager.current_database_migration_version(), None)
