import unittest

from stickshift.migration_repository import MigrationRepository, find_migration_index


class MigratinRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.migration_repository = MigrationRepository()

    def tearDown(self):
        self.migration_repository.clear()

    def test_migration_repository_create(self):
        self.migration_repository.create_repository()
        assert(self.migration_repository.is_repository_setup() == True)

    def test_migration_repository_create_fail(self):
        self.migration_repository.create_repository()
        assert(self.migration_repository.create_repository() == False)

    def test_migration_repository_clear_after_already_cleared(self):
        assert(self.migration_repository.clear() == False)

    def test_migration_repository_is_setup(self):
        assert(self.migration_repository.is_repository_setup() == False)
        self.migration_repository.create_repository()
        assert(self.migration_repository.is_repository_setup() == True)

    def test_table_creation_migration(self):
        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_migrations_list() == ["V00__create_table_test.sql"])

    def test_table_alteration_migration(self):
        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_alteration_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_migrations_list() == ["V00__alter_table_test.sql"])

    def test_procedure_creation_migration(self):
        self.migration_repository.create_repository()
        self.migration_repository.create_new_procedure_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_migrations_list() == ["V00__create_sp_test.sql"])

    def test_migration_count(self):
        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_migration("test")
        assert(self.migration_repository.current_migration_count() == 1)
        assert(self.migration_repository.current_downgrade_count() == 1)

    def test_migration_list(self):
        self.migration_repository.create_repository()
        self.migration_repository.create_new_table_migration("test")
        print(self.migration_repository.current_migrations_list())
        assert(self.migration_repository.current_migrations_list() == ["V00__create_table_test.sql"])

    def test_create_migration_double_digit_indexes(self):
        self.migration_repository.create_repository()
        for i in range(0, 11):
            self.migration_repository.create_new_table_migration("test_{0}".format(i))
        assert(find_migration_index("V10__create_table_test_1.sql") == "10")

    def test_path_for_directory_at_root_directory_with_custom_directory(self):
        custom_migration_repository = MigrationRepository(directory="custom")
        assert(custom_migration_repository.path_for_directory_at_root_directory("foo") == "custom/foo")