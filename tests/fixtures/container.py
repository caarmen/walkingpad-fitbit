import pytest

from walkingpadfitbit import container


@pytest.fixture(autouse=True)
def reset_container():
    # Reset singletons for each test.
    # https://github.com/ets-labs/python-dependency-injector/issues/421
    container.reset_singletons()
