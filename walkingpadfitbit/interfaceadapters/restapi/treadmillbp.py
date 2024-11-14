import enum
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from walkingpadfitbit.containers import Container
from walkingpadfitbit.domain.treadmillcontroller import TreadmillController
from walkingpadfitbit.interfaceadapters.restapi.flaskutils import ensure_sync

bp = Blueprint(
    "treadmill",
    __name__,
    url_prefix="/treadmill",
)


@bp.route("/start", methods=("POST",))
@bp.response(
    HTTPStatus.NO_CONTENT,
    description="The treadmill was successfully started.",
)
@ensure_sync
@inject
async def start(
    ctler: TreadmillController = Provide[Container.treadmill_controller],
) -> None:
    """
    Start the treadmill.
    """
    await ctler.start()
    return Response(status=HTTPStatus.NO_CONTENT)


@bp.route("/stop", methods=("POST",))
@bp.response(
    HTTPStatus.NO_CONTENT,
    description="The treadmill was successfully stopped.",
)
@ensure_sync
@inject
async def stop(
    ctler: TreadmillController = Provide[Container.treadmill_controller],
) -> None:
    """
    Stop the treadmill.
    """
    await ctler.stop()
    return Response(status=HTTPStatus.NO_CONTENT)


class Status(enum.StrEnum):
    started = enum.auto()
    stopped = enum.auto()


class ToggleResponseSchema(Schema):
    status = fields.Enum(enum=Status, required=True)


@bp.route("/toggle-start-stop", methods=("POST",))
@bp.response(
    HTTPStatus.OK,
    ToggleResponseSchema,
    description="The treadmill start/stop state was successfully toggled.",
)
@ensure_sync
@inject
async def toggle_start_stop(
    ctler: TreadmillController = Provide[Container.treadmill_controller],
) -> ToggleResponseSchema:
    """
    Toggle the start/stop state of the treadmill.

    If the treadmill is running, stop it.

    If the treadmill isn't running, start it.
    """
    status = None
    if ctler.is_on():
        await ctler.stop()
        status = Status.stopped
    else:
        await ctler.start()
        status = Status.started
    return ToggleResponseSchema().load({"status": status})
