import allure
import pytest
from http import HTTPStatus

from src.pydantic_schemas.error import Error
from src.pydantic_schemas.image import Image
from src.pydantic_schemas.images import Images
from src.pydantic_schemas.breeds import Breeds
from src.utils import load_json, get_test_data_path
from configuration import supported_image_formats


@allure.feature("Test dog breeds")
class TestDogBreed:
    breeds_data = load_json(get_test_data_path("breeds_list.json"))

    @allure.story("Get random dog image")
    @allure.title("Get random dog")
    @pytest.mark.image
    @pytest.mark.parametrize("image_formats", [supported_image_formats])
    def test_get_random_dog(self, dog_api, get_image_file, image_formats):

        response_obj = dog_api.get(path="/breeds/image/random")
        response_obj.assert_status_code(HTTPStatus.OK) \
            .validate_schema(Image) \
            .assert_field_value_equal("status", "success")\
            .assert_file_ext([".jpg", ".png"])

        image_url = response_obj.response_json["message"]

        image_file = get_image_file(image_url)
        response_obj.assert_is_image(image_file.headers["Content-type"], image_formats)

    @allure.story("Get breeds full list")
    @allure.title("Get all breeds")
    @pytest.mark.parametrize("breeds_list", [breeds_data])
    def test_get_all_breeds(self, dog_api, breeds_list):
        dog_api.get(path="/breeds/list/all") \
            .assert_status_code(HTTPStatus.OK) \
            .validate_schema(Breeds) \
            .assert_field_value_equal("status", "success") \
            .assert_field_value_equal("message", breeds_list)

    @allure.story("Get random sub breed image")
    @allure.title("Get random sub breed image")
    @pytest.mark.parametrize("sub_breed", [*breeds_data["hound"]])
    def test_random_sub_breed_image(self, dog_api, get_image_file, sub_breed):
        response_obj = dog_api.get(path=f"/breed/hound/{sub_breed}/images/random")
        response_obj.assert_status_code(HTTPStatus.OK)\
            .validate_schema(Image)\
            .assert_field_value_equal("status", "success")

        image_url = response_obj.response_json["message"]

        image_file = get_image_file(image_url)
        response_obj.assert_is_image(image_file.headers["Content-type"], supported_image_formats)

    @allure.story("Get images for breed")
    @allure.title("Get breed images")
    @pytest.mark.parametrize("breed", [
        *[breed for breed, sub_breed in breeds_data.items() if sub_breed][:10]
    ])
    def test_breed_images(self, dog_api, breed):
        response_obj = dog_api.get(path=f"/breed/{breed}/images")
        response_obj.assert_status_code(HTTPStatus.OK)\
            .validate_schema(Images)\
            .assert_field_value_equal("status", "success")\

        image_url_list = response_obj.response_json["message"]

        for image_url in image_url_list:
            response_obj.assert_is_true(image_url.lower().endswith(".jpg"))

    @allure.story("Get error for not existing breeds")
    @allure.title("Get images by invalid breed")
    @pytest.mark.parametrize("breed", [
        *[breed+'err' for breed, sub_breed in breeds_data.items() if sub_breed][:10]
    ])
    def test_invalid_breed_images(self, dog_api, breed):
        dog_api.get(path=f"/breed/{breed}/images")\
            .assert_status_code(HTTPStatus.NOT_FOUND)\
            .validate_schema(Error)\
            .assert_field_value_equal("status", "error")

    @allure.story("Get random images for sub breed")
    @allure.title("Get sub breed images")
    @pytest.mark.parametrize("number_of_images", [i for i in range(1, 10)])
    def test_n_random_sub_breed_image(self, dog_api, number_of_images):
        response_obj = dog_api.get(path=f"/breed/hound/english/images/random/{number_of_images}")\
            .assert_status_code(HTTPStatus.OK)\
            .validate_schema(Images) \
            .assert_field_value_equal("status", "success")

        image_url_list = response_obj.response_json["message"]
        response_obj.assert_is_true(len(image_url_list) == number_of_images)
