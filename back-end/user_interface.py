""" This file is part of Good Read Web Scraper

Contain all interface functions to interactively communicate with user
Start scraper/json/api mode according to user input
"""
import requests
import common_utility
import user_interface_utility
import database
import author_scraper
import book_scraper


def start_interface():
    """
    Function that get mode of program
    :return: None
    """
    mode_hint = "scrape -- Activate scraper and stored info in database.\n" + \
                "json -- Export data to file OR Load json file to database\n" + \
                "api -- Use api to manipulate database\n" + \
                "Please pick a mode to start\n"
    mode_valid_input = ['scrape', 'json', 'api']
    mode = input(mode_hint)
    while True:
        if user_interface_utility.check_valid_input(mode, mode_valid_input):
            break
        mode = input()
    if mode == 'scrape':
        scrape_mode()
    elif mode == 'json':
        json_mode()
    else:
        api_mode()


def scrape_mode():
    """
    Function that guide user to input arguments that scraper required
    :return: None
    """
    connected_database = database.DataBase()
    b_scraper = book_scraper.BookScraper(connected_database)
    a_scraper = author_scraper.AuthorScraper(connected_database)

    book_count_str = input('How many books do you need?\n')
    while True:
        if not common_utility.check_positive(book_count_str):
            book_count_str = input('Please provide a non negative integer.\n')
        else:
            book_count = int(book_count_str)
            break

    author_count_str = input('How many authors do you need?\n')
    while True:
        if not common_utility.check_positive(author_count_str):
            author_count_str = input('Please provide a non negative integer.\n')
        else:
            author_count = int(author_count_str)
            break

    start_url = input('Please provide a Good Read book url to start.\n')
    while True:
        if not common_utility.check_valid_start_url(start_url):
            start_url = input('This url is invalid.Please provide a Good Read book url to start.\n')
        else:
            break

    print('Scraper start.')
    b_scraper.start(book_count, start_url)
    a_scraper.start(author_count, start_url)
    print('Scraper finish.')


def json_mode():
    """
    Function that guide user to input json file path and manipulate the database accordingly
    :return:None
    """
    connected_database = database.DataBase()
    json_option_str = "Please pick a option to start\n" + \
                      "load -- Load a valid json file to the database\n" + \
                      "export -- Export all data in database to a file\n"
    json_valid_input = ['load', 'export']
    json_option = input(json_option_str)
    while True:
        if user_interface_utility.check_valid_input(json_option, json_valid_input):
            break
        json_option = input()

    if json_option == 'load':
        file_path = input('Please provide path to a valid json file\n')
        while True:
            result = common_utility.check_valid_json_file(file_path)
            if result != file_path:
                print(result)
                file_path = input('Please provide path to a valid json file\n')
            else:
                break
        connected_database.load_json_data(file_path)
    else:
        file_path = input('Please provide a path to an empty json file\n')
        while True:
            if user_interface_utility.check_valid_export_path(file_path):
                break
            file_path = input('Please provide a path to an empty json file\n')
        connected_database.export_data_json(file_path)


def api_mode():
    """
    Function that guide user to pick a request type and call handle function accordingly
    :return: None
    """
    api_option_str = "Please pick a request type to start\n" + \
                     "GET -- Get info from database\n" + \
                     "PUT -- Update info in database\n" + \
                     "POST -- Add new documents to database\n" + \
                     "DELETE -- Delete a document in database\n"
    api_valid_input = ['GET', 'PUT', 'POST', 'DELETE']
    api_option = input(api_option_str)
    while True:
        if user_interface_utility.check_valid_input(api_option, api_valid_input):
            break
        api_option = input()
    if api_option == 'GET':
        handle_get()
    elif api_option == 'PUT':
        handle_put()
    elif api_option == 'POST':
        handle_post()
    else:
        handle_delete()


def handle_get():
    """
    Function that guide user input GET request required arguments
    :return: response from server
    """
    base_url = 'http://127.0.0.1:5000/api/'
    get_option_str = "Please pick an api command to start\n" + \
                     "book -- Get info of 1 book using id\n" + \
                     "author -- Get info of 1 author using id\n" + \
                     "search -- Get info based on query string\n"
    get_valid_input = ['book', 'author', 'search']
    get_option = input(get_option_str)
    while True:
        if user_interface_utility.check_valid_input(get_option, get_valid_input):
            break
        get_option = input()
    if get_option == 'search':
        query_str = input("Please input a query string\n")
        response = requests.get(base_url + 'search', params={'q': query_str})
    else:
        input_id = user_interface_utility.get_input_id()
        response = requests.get(base_url + get_option, params={'id': input_id})

    if response.status_code == 200:
        print(response.text)
    else:
        print(response.json())


def handle_put():
    """
    Function that guide user input PUT request required arguments and body part
    :return: response from server
    """
    base_url = 'http://127.0.0.1:5000/api/'
    put_option_str = "Please pick an api command to start\n" + \
                     "book -- Update info of 1 book using id\n" + \
                     "author -- Update info of 1 author using id\n"
    put_valid_input = ['book', 'author']
    put_option = input(put_option_str)
    while True:
        if user_interface_utility.check_valid_input(put_option, put_valid_input):
            break
        put_option = input()
    input_id = user_interface_utility.get_input_id()
    json_data = user_interface_utility.get_input_json_data()
    response = requests.put(base_url + put_option,
                            json=json_data, params={'id': input_id},
                            headers={'Content-Type': "application/json",
                                     'Accept': "application/json"})
    if response.status_code == 200:
        print(response.text)
    else:
        print(response.json())


def handle_post():
    """
    Function that guide user input POST request required arguments and body part
    :return: response from server
    """
    base_url = 'http://127.0.0.1:5000/api/'
    post_option_str = "Please pick an api command to start\n" + \
                      "book -- Add 1 book document to database\n" + \
                      "books -- Add multiple book documents to database\n" + \
                      "author -- Add 1 author document to database\n" + \
                      "authors -- Add multiple author documents to database\n" + \
                      "scrape -- Use scraper to add documents to database\n"
    post_valid_input = ['book', 'books', 'author', 'authors', 'scrape']
    post_option = input(post_option_str)
    while True:
        if user_interface_utility.check_valid_input(post_option, post_valid_input):
            break
        post_option = input()

    if post_option == 'scrape':
        scrape_mode()
    else:
        json_data = user_interface_utility.get_input_json_data()
        response = requests.post(base_url + post_option, json=json_data,
                                 headers={'Content-Type': "application/json",
                                          'Accept': "application/json"})
        if response.status_code == 200:
            print(response.text)
        else:
            print(response.json())


def handle_delete():
    """
    Function that guide user input DELETE request required arguments
    :return: response from server
    """
    base_url = 'http://127.0.0.1:5000/api/'
    delete_option_str = "Please pick an api command to start\n" + \
                        "book -- Delete 1 book document using id\n" + \
                        "author -- Delete 1 author document using id\n"
    delete_valid_input = ['book', 'author']
    delete_option = input(delete_option_str)
    while True:
        if user_interface_utility.check_valid_input(delete_option, delete_valid_input):
            break
        delete_option = input()
    input_id = user_interface_utility.get_input_id()
    response = requests.delete(base_url + delete_option, params={'id': input_id})
    if response.status_code == 200:
        print(response.text)
    else:
        print(response.json())


if __name__ == "__main__":
    start_interface()
