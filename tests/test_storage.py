from storage import Storage, StorageError
import pytest


@pytest.fixture
def storage() -> Storage:
    return Storage.temporary()


def test_storage_gives_none_for_uknown_name(storage: Storage) -> None:
    assert storage.get_name_morph('name') is None


def test_storge_gives_name_datv_for_known_name(storage: Storage) -> None:
    storage.set_name_morph('name', 'known-name')
    assert storage.get_name_morph('name') == 'known-name'


def test_storage_raises_if_duplicate_name_set(storage: Storage) -> None:
    storage.set_name_morph('new-name', 'known-new-name')
    with pytest.raises(StorageError):
        storage.set_name_morph('new-name', 'known-new-name')


def test_storage_gives_new_id_for_new_webinar(storage: Storage) -> None:
    webinar = {'a': True}
    webinar_id = storage.add_webinar(webinar)
    assert webinar_id == 0


def test_storage_gives_existing_id_for_existing_webinar(
        storage: Storage,
) -> None:
    webinar = {'a': True}
    webinar_id = storage.add_webinar(webinar)
    assert storage.add_webinar(webinar) == webinar_id


def test_storage_gives_webinar_by_existing_id(storage: Storage) -> None:
    webinar = {'a': True}
    webinar_id = storage.add_webinar(webinar)
    assert storage.get_webinar(webinar_id) == webinar


def test_storage_gives_none_for_unknown_id(storage: Storage) -> None:
    assert storage.get_webinar(99) is None
