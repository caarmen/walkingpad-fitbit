import dataclasses

import pytest
from ph4_walkingpad.pad import WalkingPad

from tests.fakes.ph4_walkingpad.fakecontroller import (
    ControllerScenario,
    FakeController,
    FakeWalkingPadCurStatus,
)
from tests.fakes.ph4_walkingpad.fakescanner import FakeBLEDevice
from tests.spy import Call, Spy
from walkingpadfitbit.interfaceadapters.walkingpad.treadmillcontroller import (
    WalkingpadTreadmillController,
)


@pytest.mark.asyncio
async def test_start():
    fake_ble_device = FakeBLEDevice(address="some address")
    fake_controller = FakeController()
    walkingpad_treadmill_controller = WalkingpadTreadmillController(
        device=fake_ble_device,
        controller=fake_controller,
    )
    spy_controller = Spy(fake_controller)
    await walkingpad_treadmill_controller.start()

    assert spy_controller.method_calls == [
        Call("switch_mode", (WalkingPad.MODE_MANUAL,)),
        Call("start_belt"),
    ]


@pytest.mark.asyncio
async def test_stop():
    fake_ble_device = FakeBLEDevice(address="some address")
    fake_controller = FakeController()
    walkingpad_treadmill_controller = WalkingpadTreadmillController(
        device=fake_ble_device,
        controller=fake_controller,
    )
    spy_controller = Spy(fake_controller)
    await walkingpad_treadmill_controller.stop()

    assert spy_controller.method_calls == [
        Call("stop_belt"),
        Call("switch_mode", (WalkingPad.MODE_STANDBY,)),
    ]


@dataclasses.dataclass
class SetSpeedScenario:
    id: str
    requested_speed_kph: float
    controller_scenario: ControllerScenario
    expected_controller_method_calls: list[Call]


SET_SPEED_SCENARIOS = [
    SetSpeedScenario(
        id="set speed",
        requested_speed_kph=2.5,
        controller_scenario=ControllerScenario(),
        expected_controller_method_calls=[
            Call("change_speed", (25,)),
        ],
    ),
    SetSpeedScenario(
        id="Set speed with zero",
        requested_speed_kph=0.0,
        controller_scenario=ControllerScenario(),
        expected_controller_method_calls=[
            Call("change_speed", (0,)),
        ],
    ),
]


@pytest.mark.parametrize(
    ids=[x.id for x in SET_SPEED_SCENARIOS],
    argnames=["scenario"],
    argvalues=[[x] for x in SET_SPEED_SCENARIOS],
)
@pytest.mark.asyncio
async def test_set_speed(
    scenario: SetSpeedScenario,
):
    fake_ble_device = FakeBLEDevice(address="some address")
    fake_controller = FakeController(scenario.controller_scenario)
    walkingpad_treadmill_controller = WalkingpadTreadmillController(
        device=fake_ble_device,
        controller=fake_controller,
    )
    spy_controller = Spy(fake_controller)
    await walkingpad_treadmill_controller.set_speed(scenario.requested_speed_kph)
    assert spy_controller.method_calls == scenario.expected_controller_method_calls


@dataclasses.dataclass
class ChangeSpeedByScenario:
    id: str
    requested_speed_delta_kph: float
    controller_scenario: ControllerScenario
    expected_controller_method_calls: list[Call]


CHANGE_SPEED_BY_SCENARIOS = [
    ChangeSpeedByScenario(
        id="increase speed by 0.5",
        requested_speed_delta_kph=0.5,
        expected_controller_method_calls=[Call("change_speed", (45,))],
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=40,  # 4.0 kph
            )
        ),
    ),
    ChangeSpeedByScenario(
        id="decrease speed by 0.5",
        requested_speed_delta_kph=-0.5,
        expected_controller_method_calls=[Call("change_speed", (35,))],
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=40,  # 4.0 kph
            )
        ),
    ),
    ChangeSpeedByScenario(
        id="increase speed when no previous speed",
        requested_speed_delta_kph=0.8,
        controller_scenario=ControllerScenario(),
        expected_controller_method_calls=[Call("change_speed", (8,))],
    ),
    ChangeSpeedByScenario(
        id="decrease speed to be negative",
        requested_speed_delta_kph=-1.0,
        expected_controller_method_calls=[Call("change_speed", (0,))],
        controller_scenario=ControllerScenario(
            last_status=FakeWalkingPadCurStatus(
                dist=10,
                time=5,
                belt_state=1,
                speed=5,  # 0.5 kph
            )
        ),
    ),
]


@pytest.mark.parametrize(
    ids=[x.id for x in CHANGE_SPEED_BY_SCENARIOS],
    argnames=["scenario"],
    argvalues=[[x] for x in CHANGE_SPEED_BY_SCENARIOS],
)
@pytest.mark.asyncio
async def test_change_speed_by(
    scenario: ChangeSpeedByScenario,
):
    fake_ble_device = FakeBLEDevice(address="some address")
    fake_controller = FakeController(scenario.controller_scenario)
    walkingpad_treadmill_controller = WalkingpadTreadmillController(
        device=fake_ble_device,
        controller=fake_controller,
    )
    spy_controller = Spy(fake_controller)
    await walkingpad_treadmill_controller.change_speed_by(
        scenario.requested_speed_delta_kph
    )
    assert spy_controller.method_calls == scenario.expected_controller_method_calls
