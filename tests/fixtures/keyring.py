from typing import Generator

import pytest
from keyring import backend, set_keyring


class MemoryKeyRing(backend.KeyringBackend):
    _data: dict = {}

    def set_password(
        self,
        service: str,
        username: str,
        password: str,
    ) -> None:
        self._data[username] = password

    def get_password(
        self,
        service: str,
        username: str,
    ) -> str | None:
        return self._data[username]

    def delete_password(
        self,
        service: str,
        username: str,
    ) -> None:
        self._data.pop(username, None)

    def clear(self):
        self._data.clear()


@pytest.fixture(autouse="true")
def memory_key_ring() -> Generator[MemoryKeyRing, None, None]:
    kr = MemoryKeyRing()
    set_keyring(kr)
    yield kr
    kr.clear()
