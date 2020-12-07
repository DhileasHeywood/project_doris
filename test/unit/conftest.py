import pytest
from doris import create_app


@pytest.fixture
def app():
    """ Present the Doris app as a fixture """

    app = create_app({
        'SECRET_KEY': 'test',
        'SESSION_COOKIE_DOMAIN': None,
        'TESTING': True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
