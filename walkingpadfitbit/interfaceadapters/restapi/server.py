import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask

from walkingpadfitbit.interfaceadapters.restapi import treadmillbp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(treadmillbp.bp)
    return app


async def run_server(
    host: str = "127.0.0.1",
    port: int = 11198,
):
    server = uvicorn.Server(
        uvicorn.Config(
            WsgiToAsgi(create_app()),
            host=host,
            port=port,
        )
    )
    await server.serve()
