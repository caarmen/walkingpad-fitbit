import pytest

from tests.fakes.builtins.fakestdout import FakeStdout
from walkingpadfitbit.auth.client import Client
from walkingpadfitbit.domain.remoterepository import RemoteActivityRepository
from walkingpadfitbit.interfaceadapters.fitbit.remoterepository import (
    FitbitRemoteActivityRepository,
)


@pytest.fixture
def remote_activity_repository(
    client: Client,
) -> RemoteActivityRepository:
    return FitbitRemoteActivityRepository(client)


@pytest.fixture
def event_output() -> FakeStdout:
    return FakeStdout()
