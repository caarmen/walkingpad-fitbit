from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, Response

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
    await ctler.start()
    return Response(status=HTTPStatus.NO_CONTENT)


@bp.route("/stop", methods=("POST",))
@inject
async def stop(
    ctler: TreadmillController = Provide[Container.treadmill_controller],
):
    await ctler.stop()
    return Response(status=HTTPStatus.NO_CONTENT)
