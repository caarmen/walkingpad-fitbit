from copy import deepcopy

import uvicorn
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from asgiref.wsgi import WsgiToAsgi
from flasgger import APISpec, Swagger
from flask import Flask
from uvicorn.config import LOGGING_CONFIG

from walkingpadfitbit.interfaceadapters.restapi import treadmillbp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(treadmillbp.bp)

    spec = APISpec(
        title="Treadmill API",
        version="0.0.1",
        openapi_version="3.0.0",
        plugins=[
            FlaskPlugin(),
            MarshmallowPlugin(),
        ],
    )

    Swagger(
        app,
        config={
            **Swagger.DEFAULT_CONFIG,
            "title": spec.title,
            "specs_route": "/",
            "openapi": spec.openapi_version,
        },
        template=spec.to_flasgger(
            app,
            definitions=[
                treadmillbp.ToggleResponseSchema,
            ],
        ),
    )
    return app


async def run_server(
    host: str = "127.0.0.1",
    port: int = 11198,
):
    # Configure uvicorn to log request accesses to stderr.
    # In fact, we want all logs to stderr, to not be mixed
    # with the monitoring output of this application.
    log_config = deepcopy(LOGGING_CONFIG)
    log_config["handlers"]["access"]["stream"] = "ext://sys.stderr"

    server = uvicorn.Server(
        uvicorn.Config(
            WsgiToAsgi(create_app()),
            host=host,
            port=port,
            log_config=log_config,
        )
    )
    await server.serve()
