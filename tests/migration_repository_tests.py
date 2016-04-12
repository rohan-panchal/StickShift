import nose

from stickshift.migration_repository import MigrationRepository


def test_migration_repository_create():
    MigrationRepository.clear()
    MigrationRepository.create_repository()
    assert(MigrationRepository.is_repository_setup())


def test_migration_repository_is_setup():
    MigrationRepository.clear()
    assert(MigrationRepository.is_repository_setup() == False)
    MigrationRepository.create_repository()
    assert(MigrationRepository.is_repository_setup() == True)
