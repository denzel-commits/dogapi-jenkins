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


@pytest.fixture()
def get_dog_breeds(dog_api):
    return dog_api.get(path="/breeds/list/all")


@pytest.fixture()
def get_random_dog(dog_api):
    return dog_api.get(path="/breeds/image/random")


@pytest.fixture()
def get_random_sub_breed_image(dog_api, request):
    sub_breed = request.param
    return dog_api.get(path=f"/breed/hound/{sub_breed}/images/random")


@pytest.fixture()
def get_n_random_sub_breed_images(dog_api, request):
    n = request.param
    return dog_api.get(path=f"/breed/hound/english/images/random/{n}")


@pytest.fixture()
def get_breed_images(dog_api, request):
    breed = request.param
    return dog_api.get(path=f"/breed/{breed}/images")


def request_image_file(url):
    return requests.get(url)


@pytest.fixture()
def get_image_file():
    return request_image_file
