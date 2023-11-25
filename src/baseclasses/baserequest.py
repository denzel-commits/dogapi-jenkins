import time
import allure

import requests
from src.baseclasses.baseresponse import BaseResponse


class BaseRequest:
    def __init__(self, base_url, logger):
        self.base_url = base_url
        self.logger = logger

    @allure.step("Making {method} request to '{path}'")
    def _request(self, method, path, params=None, json=None, headers=None, retry_count=3, retry_delay=1):
        """
        Request wrapper - adds request retry and logging functionality
        """
        self.logger.info(f"Making {method} request to {path}")
        stop_flag = False
        attempt = 0

        url = f"{self.base_url}{path}"

        response = None
        while not stop_flag:
            attempt += 1
            try:
                if method == "GET":
                    response = requests.get(url, params=params, headers=headers)
                elif method == "POST":
                    response = self.post(url, json=json, headers=headers)
                elif method == "DELETE":
                    response = self.delete(url)
            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout error, retry attempt {attempt}")
            except requests.exceptions.TooManyRedirects:
                self.logger.warning(f"TooManyRedirects error, retry attempt {attempt}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error {e}")
                raise requests.exceptions.RequestException(e)

            if response.ok or attempt > retry_count:
                stop_flag = True

        if not stop_flag:
            time.sleep(retry_delay)

        return BaseResponse(response, self.logger)

    def get(self, path="/", params=None, headers=None):
        return self._request("GET", path=path, params=params, headers=headers)

    def post(self, path="/", json=None, headers=None):
        return self._request("POST", path=path, json=json, headers=headers)

    def delete(self, path="/"):
        return self._request("DELETE", path=path)
