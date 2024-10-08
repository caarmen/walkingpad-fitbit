import logging
import webbrowser

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def webbrowser_noop(monkeypatch: pytest.MonkeyPatch):
    """
    Suppress actually opening the authorization url in the browser
    during tests (it can be annoying to see the browser openining
    links many times during a test suite).
    """
    monkeypatch.setattr(
        webbrowser, "open", lambda url: logger.info(f"Browser opens {url}")
    )
