from bleak.backends.device import BLEDevice
from dependency_injector import containers, providers

from walkingpadfitbit.domain.treadmillcontroller import TreadmillController
from walkingpadfitbit.interfaceadapters.walkingpad.device import get_device
from walkingpadfitbit.interfaceadapters.walkingpad.treadmillcontroller import (
    WalkingpadTreadmillController,
)


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        modules=["walkingpadfitbit.domain.monitoring.monitor"],
    )

    device: BLEDevice = providers.Factory(
        get_device,
        config.device.name,
    )

    treadmill_controller: TreadmillController = providers.Singleton(
        WalkingpadTreadmillController,
        device,
    )
