import datetime as dt
from types import ModuleType
from typing import Any, Callable

import pytest


@pytest.fixture
def freeze_time() -> Callable[[Any, dt.datetime], None]:
    def create_frozen_time(
        mp: pytest.MonkeyPatch,
        dt_module_to_freeze: ModuleType,
        frozen_datetime: dt.datetime,
    ):
        class FrozenDate(dt.datetime):
            def now(tz):
                return frozen_datetime

        mp.setattr(dt_module_to_freeze, "datetime", FrozenDate)

    return create_frozen_time
