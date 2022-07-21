""" This file is part of Good Read Web Scraper

Contain useful function used in user_interface.py
"""
import json
import os
import common_utility


def check_valid_input(input_str: str, valid_list: list):
    """
    Check if input string is inside valid list
    Give hint if invalid input got
    :param input_str: string from user
    :param valid_list: contain all valid string
    :return: True if valid input is provided
    """
    if input_str not in valid_list:
        hint = "Please provide following input: "
        for text in valid_list:
            hint += text + ', '
        hint = hint[:-2]
        print(hint)
        return False
    return True


def check_valid_export_path(file_path: str):
    """
    Check if file path exist and is a json file
    :param file_path: path to be checked
    :return: True if path is valid
    """
    if os.path.exists(file_path) and file_path.endswith('.json'):
        return True
    return False


def get_input_id():
    """
    Get a valid id string for api mode
    :return: input id string that is valid
    """
    input_id = input("Please provide the id for query\n")
    while True:
        if common_utility.check_positive(input_id):
            break
        input_id = input("Please provide a non negative integer\n")
    return input_id


def get_input_json_data():
    """
    Get data from a valid json file for api mode
    :return: data from json file
    """
    file_path = input("Please provide path to a json file\n")
    while True:
        if check_valid_export_path(file_path):
            break
        file_path = input("Please provide a valid path\n")
    with open(file_path) as loaded_file:
        data = json.load(loaded_file)
        return data
