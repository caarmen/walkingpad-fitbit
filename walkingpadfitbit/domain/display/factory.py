import enum

from walkingpadfitbit.domain.display.base import BaseDisplay
from walkingpadfitbit.domain.display.json import JsonDisplay
from walkingpadfitbit.domain.display.plaintext import PlainTextDisplay
from walkingpadfitbit.domain.display.richtext import RichTextDisplay


class DisplayMode(enum.StrEnum):
    PLAIN_TEXT = "plaintext"
    RICH_TEXT = "richtext"
    JSON = "json"


def get_display(display_mode: DisplayMode) -> BaseDisplay:
    if display_mode == DisplayMode.PLAIN_TEXT:
        return PlainTextDisplay()
    if display_mode == DisplayMode.RICH_TEXT:
        return RichTextDisplay()
    return JsonDisplay()
