import pytest

from main import app


@pytest.fixture
def application():
    app.config.update({
        'TESTING': True
    })

    yield app


@pytest.fixture
def client(application):
    return application.test_client()
