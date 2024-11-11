from copy import deepcopy

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_smorest import Api
from uvicorn.config import LOGGING_CONFIG

from walkingpadfitbit.interfaceadapters.restapi import treadmillbp


def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "Treadmill API"
    app.config["API_VERSION"] = "0.0.1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    api = Api(app)
    api.DEFAULT_ERROR_RESPONSE_NAME = None
    # Remove built-in schemas from smorest: we don't use them.
    api.spec.components.schemas.clear()
    api.register_blueprint(treadmillbp.bp)

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
