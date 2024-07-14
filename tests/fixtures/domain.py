import pytest

from walkingpadfitbit.auth.client import Client
from walkingpadfitbit.domain.eventhandler import TreadmillEventHandler
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
def treadmill_event_handler(
    remote_activity_repository: RemoteActivityRepository,
) -> TreadmillEventHandler:
    return TreadmillEventHandler(remote_activity_repository)
