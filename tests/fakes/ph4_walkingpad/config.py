import pytest
from ph4_walkingpad.pad import Controller, Scanner

from tests.fakes.ph4_walkingpad.fakecontroller import ControllerScenario, FakeController
from tests.fakes.ph4_walkingpad.fakescanner import FakeScanner, ScannerScenario


def configure_fake_walkingpad(
    mp: pytest.MonkeyPatch,
    scanner_scenario: ScannerScenario | None = None,
    controller_scenario: ControllerScenario | None = None,
):
    """
    Use fake replacements for walkingpad apis
    """
    mp.setattr(Scanner, "__new__", lambda _: FakeScanner(scanner_scenario))
    mp.setattr(Controller, "__new__", lambda _: FakeController(controller_scenario))
