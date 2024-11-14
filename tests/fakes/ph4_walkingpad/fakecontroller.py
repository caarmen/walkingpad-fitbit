from dataclasses import dataclass

from tests.fakes.bleak.fakebleakclient import FakeBleakClient


@dataclass
class FakeWalkingPadCurStatus:
    dist: float
    time: int
    belt_state: int
    speed: int


@dataclass
class ControllerScenario:
    cur_statuses: list[FakeWalkingPadCurStatus] | None = None
    is_connected_values: list[bool] | None = None
    run_exceptions: list[Exception | None] = None
    last_status: FakeWalkingPadCurStatus | None = None


class FakeController:
    """Controller test double"""

    def __init__(self, scenario: ControllerScenario | None = None) -> None:
        self.scenario = scenario if scenario else ControllerScenario()
        self.run_iterations = 0
        self.ask_stats_iterations = 0
        self.last_status = self.scenario.last_status

    async def run(self, *args, **kwargs):
        if self.scenario.run_exceptions and self.run_iterations < len(
            self.scenario.run_exceptions
        ):
            exception_to_raise = self.scenario.run_exceptions[self.run_iterations]
            self.run_iterations += 1
            if exception_to_raise:
                raise exception_to_raise

        self.client = FakeBleakClient(
            fake_is_connected_values=self.scenario.is_connected_values
        )

    async def ask_stats(self, *args, **kwargs):
        if self.ask_stats_iterations < len(self.scenario.cur_statuses):
            self.handler_cur_status(
                None, self.scenario.cur_statuses[self.ask_stats_iterations]
            )
            self.ask_stats_iterations += 1

    async def disconnect(self): ...

    async def switch_mode(self, mode: int): ...

    async def start_belt(self): ...

    async def stop_belt(self): ...

    async def change_speed(self, speed: int): ...
