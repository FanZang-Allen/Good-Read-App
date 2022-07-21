""" This file is part of Good Read Web Scraper

Contain useful function used in web_api.py
"""
from flask import request
from flask_restful import abort
from query_parser import parse_query_string
from common_utility import check_positive


def check_json_content_type():
    """
    Function that check if content type in request is set correctly
    """
    if request.content_type != "application/json":
        abort(415, error_message="Content type should be application/json")


def check_valid_id(connected_database, collection_name):
    """
    Function that check if id exist in query args and if id is valid
    """
    if 'id' not in request.args:
        abort(400, error_message="Query arg: " + collection_name + " Id required")

    try:
        got_id = int(request.args.get('id', None))
    except (TypeError, ValueError):
        abort(400, error_message=collection_name + " Id should be an integer value")

    curr_collection = connected_database.database[collection_name]
    if curr_collection.count_documents({'id': str(got_id)}, limit=1) == 0:
        abort(404, error_message=collection_name + " not exists")

    return str(got_id)


def check_valid_scrape_args(required_args):
    """
    Function that check if all args for scraper is provided in query args
    :param required_args: args list
    :return: parsed arg list if all args are valid
    """
    parsed_args = []
    for arg in required_args:
        if arg not in request.args:
            abort(400, error_message="Query arg: " + arg + " required")

        if arg == 'start_url':
            try:
                given_url = str(request.args.get(arg, None))
                if not given_url.startswith('https://www.goodreads.com/book'):
                    abort(400, error_message="Please provide a good read book url")
                parsed_args.append(given_url)
            except (TypeError, ValueError):
                abort(400, error_message=arg + " should be a string")
        else:
            try:
                given_count = int(request.args.get(arg, None))
                if given_count < 0:
                    abort(400, error_message=arg + " should not be negative")
                parsed_args.append(given_count)
            except (TypeError, ValueError):
                abort(400, error_message=arg + " should be an integer")
    return parsed_args


def check_valid_query_string():
    """
    Check if query string is provided in query arg
    Check if query string satisfy language requirement
    :return: query result based on input string or error message
    """
    if 'q' not in request.args:
        return False, {'error_message': 'Query arg: q is required'}
    input_str = str(request.args.get('q'))
    parsed_result = parse_query_string(input_str)
    if parsed_result is None:
        return False, {'error_message': 'Given query string is not valid'}
    result = {'collection_name': parsed_result[0], 'expression': parsed_result[1]}
    return True, result


def check_valid_k_argument():
    """
    Check if k argument is provided in request
    :return: False if incorrect value k is provided
    """
    if 'k' not in request.args:
        return False, {'error_message': 'Query arg: k is required'}
    k_str = str(request.args.get('k'))
    if not check_positive(k_str):
        return False, {'error_message': 'Query arg: k is not valid'}
    return True, {'k_arg': int(k_str)}
