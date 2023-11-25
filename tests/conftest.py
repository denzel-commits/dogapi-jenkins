import pytest
import requests

from src.baseclasses.baserequest import BaseRequest
from src.logger import Logger


def pytest_addoption(parser):
    parser.addoption("--logging-level", default="WARNING")


@pytest.fixture()
def logger(request):
    log_level = request.config.getoption("--logging-level")

    return Logger(request.node.name, log_level).get_logger()


@pytest.fixture()
def dog_api(logger):
    return BaseRequest(base_url="https://dog.ceo/api", logger=logger)


def request_image_file(url):
    return requests.get(url)


@pytest.fixture()
def get_image_file():
    return request_image_file
