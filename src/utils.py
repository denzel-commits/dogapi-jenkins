import csv
import json
import os

from configuration import TEST_DATA_PATH


def load_json(filename):
    with open(filename, "r", encoding="UTF-8") as json_file:
        data = json.load(json_file)

    return data


def load_cvs(filename):
    with open(filename, "r", encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        data_list = [tuple(row) for row in csv_reader]

    return data_list


def load_cvs_dict(filename):
    with open(filename, "r", encoding="UTF-8") as csv_file:
        dict_reader = csv.DictReader(csv_file)
        list_of_dict = list(dict_reader)

    return list_of_dict


def get_test_data_path(filename):
    return os.path.join(TEST_DATA_PATH, filename)


