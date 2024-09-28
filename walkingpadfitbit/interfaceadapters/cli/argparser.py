import argparse
from typing import Protocol

from walkingpadfitbit.domain.display.factory import DisplayMode


class CliArgs(Protocol):
    device_name: str
    monitor_duration_s: float
    poll_interval_s: float
    display_mode: DisplayMode


def parse_args() -> CliArgs:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "device_name",
        help="Name of the walkingpad device (ex: KS-ST-A1P).",
        type=str,
    )
    arg_parser.add_argument(
        "-d",
        "--monitor-duration",
        help="Monitoring duration in seconds. By default the program monitors forever.",
        type=float,
        default=None,
        dest="monitor_duration_s",
    )
    arg_parser.add_argument(
        "-p",
        "--poll-interval",
        help="Poll interval in seconds (default %(default)s).",
        type=float,
        default=1.0,
        dest="poll_interval_s",
    )
    arg_parser.add_argument(
        "-m",
        "--display-mode",
        help="Display mode",
        type=DisplayMode,
        choices=DisplayMode,
        default=DisplayMode.RICH_TEXT,
    )

    return arg_parser.parse_args()
