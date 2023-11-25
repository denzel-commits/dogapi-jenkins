import os.path

PROJECT_ROOT = os.path.dirname(__file__)
TEST_DATA_PATH = os.path.join(PROJECT_ROOT, "test_data")
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "logs")

LOGGING_LEVEL = "INFO"

supported_image_formats = ("image/png", "image/jpeg", "image/gif")
