import nose

from stickshift.migration_repository import MigrationRepository


def test_migration_repository_create():
    MigrationRepository.clear()
    MigrationRepository.create_repository()
    assert(MigrationRepository.is_repository_setup() == True)


def test_migration_repository_create_fail():
    MigrationRepository.clear()
    MigrationRepository.create_repository()
    assert(MigrationRepository.create_repository() == False)


def test_migration_repository_clear_false():
    MigrationRepository.clear()
    assert(MigrationRepository.clear() == False)


def test_migration_repository_is_setup():
    MigrationRepository.clear()
    assert(MigrationRepository.is_repository_setup() == False)
    MigrationRepository.create_repository()
    assert(MigrationRepository.is_repository_setup() == True)


def test_table_creation_migration():
    MigrationRepository.clear()

    MigrationRepository.create_repository()
    MigrationRepository.create_new_table_migration("test")
    assert(MigrationRepository.current_migration_count() == 1)
    assert(MigrationRepository.current_migrations_list() == ["V00__create_table_test.sql"])


def test_table_alteration_migration():
    MigrationRepository.clear()

    MigrationRepository.create_repository()
    MigrationRepository.create_new_table_alteration_migration("test")
    assert(MigrationRepository.current_migration_count() == 1)
    assert(MigrationRepository.current_migrations_list() == ["V00__alter_table_test.sql"])


def test_procedure_creation_migration():
    MigrationRepository.clear()

    MigrationRepository.create_repository()
    MigrationRepository.create_new_procedure_migration("test")
    assert(MigrationRepository.current_migration_count() == 1)
    assert(MigrationRepository.current_migrations_list() == ["V00__create_sp_test.sql"])


def test_migration_count():
    MigrationRepository.clear()

    MigrationRepository.create_repository()
    MigrationRepository.create_new_table_migration("test")
    assert(MigrationRepository.current_migration_count() == 1)
    assert(MigrationRepository.current_downgrade_count() == 1)


def test_migration_list():
    MigrationRepository.clear()

    MigrationRepository.create_repository()
    MigrationRepository.create_new_table_migration("test")
    print(MigrationRepository.current_migrations_list())
    assert(MigrationRepository.current_migrations_list() == ["V00__create_table_test.sql"])


def test_database_config():
    MigrationRepository.clear()

    MigrationRepository.create_repository()
    config = MigrationRepository.database_config("DATABASE")
    assert(cmp(config, {
        "host": "DB_HOST",
        "port": "DB_PORT",
        "username": "DB_USERNAME",
        "password": "DB_PASSWORD",
        "database": "DB_NAME"}) == 0)
