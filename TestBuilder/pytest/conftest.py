import pytest

from bravado.client import SwaggerClient

# TODO: remove
if False:
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture
def client():
    return SwaggerClient.from_url('http://localhost:8080/swagger.json', config={'also_return_response': True})

pytest_plugins = "_pytest.pytester"