import datetime as dt
from types import ModuleType
from typing import Any, Callable
from zoneinfo import ZoneInfo

import pytest


@pytest.fixture
def freeze_time() -> (
    Callable[[pytest.MonkeyPatch, ModuleType, tuple[Any], dt.timezone], None]
):
    def create_frozen_time(
        mp: pytest.MonkeyPatch,
        dt_module_to_freeze: ModuleType,
        frozen_datetime_args: tuple[Any],
        local_timezone: ZoneInfo = ZoneInfo("UTC"),
    ):
        class FrozenDate(dt.datetime):
            def now(tz):
                return FrozenDate(*frozen_datetime_args, tzinfo=tz)

            def astimezone(self):
                return super().astimezone(tz=local_timezone)

        mp.setattr(dt_module_to_freeze, "datetime", FrozenDate)

    return create_frozen_time
