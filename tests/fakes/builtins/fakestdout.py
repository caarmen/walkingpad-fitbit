from io import TextIOBase


class FakeStdout(TextIOBase):
    def __init__(self):
        self.lines_written = ""

    def write(self, s: str) -> int:
        self.lines_written += s
        return len(s)
