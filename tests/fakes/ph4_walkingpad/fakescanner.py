from dataclasses import dataclass

from bleak.backends.device import BLEDevice


class FakeBLEDevice(BLEDevice):
    def __init__(self, address: str = "some address"):
        super().__init__(address, name=None, details=None, rssi=0)


@dataclass
class ScannerScenario:
    found_addresses: list[str] | None = None


class FakeScanner:
    """Scanner test double"""

    def __init__(self, scenario: ScannerScenario | None = None) -> None:
        self.scenario = scenario if scenario else ScannerScenario()

    async def scan(self, *args, **kwargs):
        self.walking_belt_candidates = []
        if self.scenario.found_addresses:
            for found_address in self.scenario.found_addresses:
                self.walking_belt_candidates.append(FakeBLEDevice(found_address))
