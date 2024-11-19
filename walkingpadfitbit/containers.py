from bleak.backends.device import BLEDevice
from dependency_injector import containers, providers
from ph4_walkingpad.pad import Controller, Scanner

from walkingpadfitbit.domain.treadmillcontroller import TreadmillController
from walkingpadfitbit.interfaceadapters.walkingpad.device import (
    ScannerProtocol,
    get_device,
)
from walkingpadfitbit.interfaceadapters.walkingpad.treadmillcontroller import (
    ControllerProtocol,
    WalkingpadTreadmillController,
)


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        modules=[
            "walkingpadfitbit.domain.monitoring.monitor",
            "walkingpadfitbit.interfaceadapters.restapi.treadmillbp",
        ],
    )

    scanner: ScannerProtocol = providers.Singleton(
        Scanner,
    )

    device: BLEDevice = providers.Factory(
        get_device,
        config.device.name,
        scanner,
    )

    controller: ControllerProtocol = providers.Singleton(
        Controller,
    )

    treadmill_controller: TreadmillController = providers.Singleton(
        WalkingpadTreadmillController,
        device,
        controller,
    )
