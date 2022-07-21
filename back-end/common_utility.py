"""This file is part of Good Read Web Scraper

Contain common useful function for other files
"""
import json
from pathlib import Path


def check_valid_info_dict(info, collection_name):
    """
    Check given info dictionary has valid data structure and attributes type
    :param info: info data to be checked
    :param collection_name: name of collection in database
    :return: True if valid
    """
    book_float_key = ['id', 'ISBN', 'rating', 'rating_count', 'review_count']
    author_float_key = ['id', 'rating', 'rating_count', 'review_count']
    if not isinstance(info, dict):
        return False
    if 'id' not in info:
        return False

    if collection_name == 'Book':
        check_list = book_float_key
    elif collection_name == 'Author':
        check_list = author_float_key
    else:
        return False

    for key in info:
        if isinstance(info[key], list):
            if not all(isinstance(elem, str) for elem in info[key]):
                return False
            continue
        if not isinstance(info[key], str):
            return False
        # Key in check list need to be able to convert to float
        if key in check_list:
            if not check_positive(info[key]):
                return False

    return True


def check_positive(value: str):
    """
    Check if given value is greater or equal to 0
    :param value: value in string
    :return: int(value)
    """
    try:
        return float(value) >= 0
    except ValueError:
        return False


def check_valid_start_url(url):
    """
    Check if url is a good read book page
    :param url: url from parser
    :return: str(url)
    """
    try:
        start_url = str(url)
        return start_url.startswith('https://www.goodreads.com/book')
    except ValueError:
        return False


def check_valid_json_file(file_path):
    """
    Check if given path is a valid json file that is recognizable for database
    :param file_path: path from parser
    :return: file_path if valid
    """
    file = Path(file_path)
    if not file.is_file():
        return file_path + ' is not a valid path'

    with open(file_path) as open_file:
        try:
            data = json.load(open_file)
        except ValueError:
            return file_path + ' is not a valid json file'

        allowed_key = ['Book', 'Author']

        if not isinstance(data, dict):
            return file_path + ' is invalid'

        for key in data:
            if key in allowed_key:
                info_list = data[key]
                if isinstance(info_list, list):
                    for info in info_list:
                        if isinstance(info, dict):
                            if not check_valid_info_dict(info, key):
                                return file_path + 'contain invalid dict'
                        else:
                            return file_path + ' is invalid'
                else:
                    return file_path + ' is invalid'
            else:
                return file_path + ' has unrecognizable key'
    return file_path
