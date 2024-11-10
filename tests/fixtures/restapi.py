import pytest
from flask import Flask
from flask.testing import FlaskClient

from walkingpadfitbit.interfaceadapters.restapi.server import create_app


@pytest.fixture
def app() -> Flask:
    return create_app()


@pytest.fixture
def restapi_client(app: Flask) -> FlaskClient:
    return app.test_client()
