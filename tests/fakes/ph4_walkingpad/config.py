import pytest
from ph4_walkingpad.pad import Controller, Scanner

from tests.fakes.ph4_walkingpad.fakecontroller import ControllerScenario, FakeController
from tests.fakes.ph4_walkingpad.fakescanner import FakeScanner, ScannerScenario


def configure_fake_walkingpad(
    mp: pytest.MonkeyPatch,
    scanner_scenario: ScannerScenario | None = None,
    controller_scenario: ControllerScenario | None = None,
) -> tuple[FakeScanner, FakeController]:
    """
    Use fake replacements for walkingpad apis
    """
    fake_scanner = FakeScanner(scanner_scenario)
    fake_controller = FakeController(controller_scenario)
    mp.setattr(Scanner, "__new__", lambda _: fake_scanner)
    mp.setattr(Controller, "__new__", lambda _: fake_controller)
    return fake_scanner, fake_controller
