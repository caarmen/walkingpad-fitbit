from dataclasses import dataclass
from typing import Callable

import pytest
from ph4_walkingpad.pad import Controller, Scanner


@dataclass
class FakeBLEDevice:
    address: str


@dataclass
class FakeWalkingPadCurStatus:
    dist: float
    time: int
    belt_state: int


@dataclass
class WalkingPadScenario:
    found_addresses: list[str] | None = None
    cur_statuses: list[FakeWalkingPadCurStatus] | None = None


@pytest.fixture
def fake_walking_pad() -> Callable[[pytest.MonkeyPatch, WalkingPadScenario], None]:
    """
    Use fake replacements for walkingpad apis
    """

    def create_fake_walkingpad(
        mp: pytest.MonkeyPatch,
        scenario: WalkingPadScenario,
    ):
        # Fake the results of the Scanner.scan() to find the addresses configured in the scenario
        async def scanner_fake_scan(self, *args, **kwargs):
            self.walking_belt_candidates = []
            if scenario.found_addresses:
                for found_address in scenario.found_addresses:
                    self.walking_belt_candidates.append(
                        FakeBLEDevice(address=found_address)
                    )

        mp.setattr(Scanner, "scan", scanner_fake_scan)

        # Make the Controller.run() method a no-op
        async def controller_fake_run(self, *args, **kwargs):
            pass

        mp.setattr(Controller, "run", controller_fake_run)

        # Fake the Controller.ask_stats() method to return the stats configured in the scenario.
        iterations = 0

        async def controller_fake_ask_stats(self):
            nonlocal iterations
            if iterations < len(scenario.cur_statuses):
                self.handler_cur_status(None, scenario.cur_statuses[iterations])
                iterations += 1

        mp.setattr(Controller, "ask_stats", controller_fake_ask_stats)

    return create_fake_walkingpad