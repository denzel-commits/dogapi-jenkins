import allure
from pydantic import ValidationError


class BaseResponse:
    def __init__(self, response, logger):
        self.response = response
        self.response_json = response.json()
        self.response_status = response.status_code
        self.logger = logger

    @allure.step("Verify response status code to be {status_code}")
    def assert_status_code(self, status_code):
        self.logger.info(f"Verify response status code {self.response_status} to be {status_code}")
        assert self.response_status == status_code, f"{self.response_status} is not equal to {status_code}"
        return self

    @allure.step("Validate response JSON schema")
    def validate_schema(self, schema):
        self.logger.info(f"Validate response JSON schema")
        if isinstance(self.response_json, list):
            for item in self.response_json:
                try:
                    schema.model_validate(item)
                except ValidationError as e:
                    self.logger.error("Response json schema didn't pass validation", exc_info=True)
                    raise AssertionError(e)
        else:
            try:
                schema.model_validate(self.response_json)
            except ValidationError as e:
                self.logger.error("Response json schema didn't pass validation", exc_info=True)
                raise AssertionError(e)
        return self

    @allure.step("Validate file extension to be {expected_extension}")
    def assert_file_ext(self, expected_extension):
        file_url = self.response_json["message"].lower()

        self.logger.info(f"Validate file '{file_url}' extension to be {expected_extension}")

        if isinstance(expected_extension, list):
            assert file_url[file_url.rfind("."):] in expected_extension \
                    , f"File '{file_url}' doesn't have expected extension {expected_extension}"
        else:
            assert file_url.endswith(
               expected_extension), f"File '{file_url}' doesn't have expected extension {expected_extension}"

    @allure.step("Validate response {field} field to be {expected_data}")
    def assert_field_value_equal(self, field, expected_data):
        self.logger.info(f"Validate response {field} field to be {expected_data}")
        assert self.response_json[field] == expected_data, f"{self.response_json[field]} is not equal to {expected_data}"
        return self

    @allure.step("Validate {expected_condition} is True ")
    def assert_is_true(self, expected_condition):
        self.logger.info(f"Validate {expected_condition} is True")
        assert expected_condition is True, f"{expected_condition} is Falsy"
        return self

    @allure.step("Validate image Content-type {image_format} is in {expected_image_formats}")
    def assert_is_image(self, image_format, expected_image_formats):
        self.logger.info(f"Validate image Content-type {image_format} is in {expected_image_formats}")
        assert image_format in expected_image_formats, f"Document returned is not an image: {self.response_json['message']}"
        return self

    def __str__(self):
        return f"\nStatus code: {self.response_status} \n" \
               f"Requested url: {self.response.url} \n" \
               f"Response body: {self.response_json}"
