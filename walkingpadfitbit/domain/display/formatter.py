from walkingpadfitbit.domain.entities.event import TreadmillEvent


def friendly_duration(duration_s: int) -> str:
    """
    Return a friendly display of the duration.

    If the duration is less than one minute long, returns a string in the format 00:00:ss.
    Otherwise, returns a string in the format hh:mm:ss.

    :param: duration_s the duration in seconds
    :return: the friendly display.
    """
    hours, remainder_s = divmod(duration_s, 3600)
    minutes = remainder_s // 60

    if hours == 0:
        return f"{minutes}m"

    return f"{hours}h {minutes}m"


def format_duration(event: TreadmillEvent) -> str:
    return f"Duration: {friendly_duration(event.time_s)}"


def format_distance(event: TreadmillEvent) -> str:
    return f"Distance: {event.dist_km:.2f} km"


def format_speed(event: TreadmillEvent) -> str:
    return f"Speed: {event.speed_kph:.1f} km/h"
