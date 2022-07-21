""" This file is part of Good Read Web Scraper

Query parser analyse the given query string and generate query expression
for database if valid. Return None if parse failed due to invalid input string
"""
import re
import common_utility


def parse_query_string(input_str: str):
    """
    Main function to parsed a input string and return None if failed
    :param input_str: string that needed to be parsed
    :return: query expression or None if input str is invalid
    """
    # Check if logical operator exist first
    logic_operator = parse_logic_operator(input_str)

    # None means that input str is invalid
    if logic_operator is None:
        return False

    # If NOT exist, parsed string without NOT
    if logic_operator == 'NOT':
        remove_logic_str = input_str.replace('NOT', '', 1).strip()
        parsed_result = parse_no_logic_string(remove_logic_str)
        if parsed_result is None:
            return None
        no_not_exp = parsed_result[1]
        not_expression = {}
        for key in no_not_exp:
            not_expression[key] = {'$not': no_not_exp[key]}
        parsed_result[1] = not_expression
        return parsed_result

    # If AND or OR exists, parsed both left and right string
    if logic_operator == 'AND' or logic_operator == 'OR':
        left_str = input_str.split(logic_operator, 1)[0].strip()
        right_str = input_str.split(logic_operator, 1)[1].strip()
        left_result = parse_no_logic_string(left_str)
        right_result = parse_no_logic_string(right_str)
        if left_result is None or right_result is None:
            return None
        # different collection name in two side is not allowed
        if left_result[0] != right_result[0]:
            return None
        final_expression = {'$' + logic_operator.lower(): [left_result[1], right_result[1]]}
        return [left_result[0], final_expression]

    # If no logical operator exist, directly parsed the string
    parsed_result = parse_no_logic_string(input_str.strip())
    return parsed_result


def parse_logic_operator(input_str: str):
    """
    Check if content part has logical operator using regex
    :param input_str: string that needed to be parsed
    :return: Logical operator str or None if invalid input str
    """
    not_pattern = re.compile("^.*NOT.*$")
    and_pattern = re.compile("^.*AND.*$")
    or_pattern = re.compile("^.*OR.*$")
    # Only 1 operator should exist in input string
    if not_pattern.match(input_str):
        if and_pattern.match(input_str) or or_pattern.match(input_str):
            return None
        return 'NOT'

    if and_pattern.match(input_str):
        if not_pattern.match(input_str) or or_pattern.match(input_str):
            return None
        return 'AND'

    if or_pattern.match(input_str):
        if not_pattern.match(input_str) or and_pattern.match(input_str):
            return None
        return 'OR'
    return 'None'


def parse_no_logic_string(input_str: str):
    """
    Parse a query string without logical operator
    :param input_str: string that needed to be parsed
    :return: collection name and expression in a list, None if invalid string
    """
    collection_name = parse_collection_name(input_str)
    if collection_name is None:
        return None
    field = parse_field(input_str, collection_name)
    if field is None:
        return None
    expression = parse_content(input_str, field)
    if expression is None:
        return None
    return [collection_name, expression]


def parse_collection_name(input_str: str):
    """
    Get collection name using the first appeared dot operator.
    :param input_str: string that needed to be parsed
    :return: None if no valid collection name got
    """
    valid_collection_name = ['book', 'author']
    parsed_result = input_str.strip().split('.', 1)[0]
    if parsed_result not in valid_collection_name:
        return None
    collection_name = parsed_result.capitalize()
    return collection_name


def parse_field(input_str: str, collection_name: str):
    """
    Get field name using first appeared colon operator
    :param input_str: string that needed to be parsed
    :param collection_name: got name from parse_collection_name
    :return: None if no valid field name exist
    """
    # Allowed book fields
    valid_book_key = ['book_url', 'id', 'title', 'ISBN', 'author', 'author_url', 'rating',
                      'rating_count', 'review_count', 'image_url', 'similar_books']

    # Allowed author fields
    valid_author_key = ['id', 'author_name', 'rating', 'rating_count', 'review_count',
                        'image_url', 'author_books', 'related_authors']

    valid_field_dict = {'Book': valid_book_key, 'Author': valid_author_key}

    remove_object_str = input_str.strip().split('.', 1)[1].strip()
    field_result = remove_object_str.split(':', 1)[0].strip()
    if field_result not in valid_field_dict[collection_name]:
        return None
    return field_result


def parse_content(input_str: str, field: str):
    """
    Get expression based on content string
    :param input_str: string that needed to be parsed
    :param field: got field from parse_field
    :return: None if invalid content is provided
    """
    # Name of key that is allowed to be compared with number
    valid_float_key = ['id', 'rating', 'rating_count', 'review_count']

    content = input_str.strip().split(':', 1)[1].strip()
    if content == '':
        return None

    # Check if comparison operator exist using regex
    greater_pattern = re.compile("^>")
    smaller_pattern = re.compile("^<")
    quote_pattern = re.compile('^\".*\"$')

    compare_op = None
    remove_comparison_str = content.strip()
    if greater_pattern.match(content):
        compare_op = '$gt'
        remove_comparison_str = content.replace('>', '', 1).strip()
    elif smaller_pattern.match(content):
        compare_op = '$lt'
        remove_comparison_str = content.replace('<', '', 1).strip()

    if compare_op is not None:
        if quote_pattern.match(remove_comparison_str):
            # quote is not allowed when comparison operator is provided
            return None
        if field not in valid_float_key:
            # given field does not support comparison operator
            return None
        if not common_utility.check_positive(remove_comparison_str):
            # given string cannot be converted to float
            return None
        comp_float = float(remove_comparison_str)
        result_exp = {'$expr': {compare_op: [{'$toDouble': f'${field}'}, comp_float]}}
        return result_exp

    if quote_pattern.match(remove_comparison_str):
        remove_quote_str = remove_comparison_str[1:-1].strip()
        # regex representing the exact match
        return {field: {"$regex": f'^{remove_quote_str}$'}}

    # regex representing required filed contain substring
    return {field: {"$regex": f'^.*{remove_comparison_str}.*$'}}
