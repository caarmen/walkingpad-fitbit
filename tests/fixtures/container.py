import pytest

from tests.fakes.ph4_walkingpad.fakecontroller import FakeController
from tests.fakes.ph4_walkingpad.fakescanner import FakeScanner, ScannerScenario
from walkingpadfitbit import container


@pytest.fixture(autouse=True)
def reset_container():
    # Reset singletons for each test.
    # https://github.com/ets-labs/python-dependency-injector/issues/421
    container.reset_singletons()

    # Configure our DI to use fake implementations
    container.config.set("device.name", "some device")
    container.scanner.override(
        FakeScanner(ScannerScenario(found_addresses=["some address"]))
    )
    container.controller.override(FakeController())
