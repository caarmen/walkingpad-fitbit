import enum
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, Response, jsonify
from marshmallow import Schema, fields

from walkingpadfitbit.containers import Container
from walkingpadfitbit.domain.treadmillcontroller import TreadmillController

bp = Blueprint(
    "treadmill",
    __name__,
    url_prefix="/treadmill",
)


@bp.route("/start", methods=("POST",))
@inject
async def start(
    ctler: TreadmillController = Provide[Container.treadmill_controller],
):
    """
    Start the treadmill.
    ---
    responses:
      204:
        description: The treadmill was successfully started.
    """
    await ctler.start()
    return Response(status=HTTPStatus.NO_CONTENT)


@bp.route("/stop", methods=("POST",))
@inject
async def stop(
    ctler: TreadmillController = Provide[Container.treadmill_controller],
):
    """
    Stop the treadmill.
    ---
    responses:
      204:
        description: The treadmill was successfully stopped.
    """
    await ctler.stop()
    return Response(status=HTTPStatus.NO_CONTENT)


class Status(enum.StrEnum):
    started = enum.auto()
    stopped = enum.auto()


class ToggleResponseSchema(Schema):
    status = fields.Enum(enum=Status, required=True)


@bp.route("/toggle-start-stop", methods=("POST",))
@inject
async def toggle_start_stop(
    ctler: TreadmillController = Provide[Container.treadmill_controller],
):
    """
    Toggle the start/stop state of the treadmill.
    If the treadmill is running, stop it.
    If the treadmill isn't running, start it.
    ---
    responses:
      200:
        description: The treadmill start/stop state was successfully toggled.
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ToggleResponse"
    """
    status = None
    if ctler.is_on():
        await ctler.stop()
        status = Status.stopped
    else:
        await ctler.start()
        status = Status.started
    return jsonify(ToggleResponseSchema().dump({"status": status}))
