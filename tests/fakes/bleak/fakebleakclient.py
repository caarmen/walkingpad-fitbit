class FakeBleakClient:
    """BleakClient test double"""

    def __init__(self, fake_is_connected_values: list[bool] | None = None):
        self.is_connected_values = (
            fake_is_connected_values if fake_is_connected_values else [True]
        )

    @property
    def is_connected(self):
        result = self.is_connected_values[0]
        if len(self.is_connected_values) > 1:
            self.is_connected_values.pop(0)
        return result

    async def disconnect(self):
        pass
