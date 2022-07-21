""" This file is part of Good Read Web Scraper

Local web sever to handle good read api request
"""
from flask import Flask, request
from flask_restful import Api, Resource, abort
from flask_cors import CORS, cross_origin
import database
import common_utility
import web_api_utility
import author_scraper
import book_scraper
import pymongo

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

connected_database = database.DataBase()


class Book(Resource):
    """
    Resource class that handle "/api/book" request
    """
    collection_name = "Book"

    def get(self):
        """
        Get 1 book info according to id
        :return: query result from database or error message
        """
        book_id = web_api_utility.check_valid_id(connected_database, self.collection_name)
        curr_collection = connected_database.database[self.collection_name]
        result = curr_collection.find_one({"id": book_id}, {'_id': 0})
        return {'Query Result': [result]}, 200

    def put(self):
        """
        Update a exist book document using json in request body
        :return: success response or error message
        """
        book_id = web_api_utility.check_valid_id(connected_database, self.collection_name)
        web_api_utility.check_json_content_type()
        data = request.get_json()
        data['id'] = book_id
        if not common_utility.check_valid_info_dict(data, self.collection_name):
            abort(400, error_message="Provided data is not in correct format")
        connected_database.update_data(data, "Book")
        return {"Response": "Put success"}, 200

    def post(self):
        """
        Add 1 book document using json in request body
        :return: success response or error message
        """
        web_api_utility.check_json_content_type()
        data = request.get_json()
        if not common_utility.check_valid_info_dict(data, self.collection_name):
            abort(400, error_message="Provided data is not in correct format")
        connected_database.add_data(data, self.collection_name)
        return {"Response": "Post success"}, 200

    def delete(self):
        """
        Delete 1 book document using id
        :return: success response or error message
        """
        book_id = web_api_utility.check_valid_id(connected_database, self.collection_name)
        connected_database.delete_data(self.collection_name, book_id)
        return {"Response": "Delete success"}, 200


api.add_resource(Book, "/api/book")


class Author(Resource):
    """
    Resource class that handle "/api/author" request
    """
    collection_name = "Author"

    def get(self):
        """
        Get 1 author info according to id
        :return: query result from database or error message
        """
        author_id = web_api_utility.check_valid_id(connected_database, self.collection_name)
        curr_collection = connected_database.database[self.collection_name]
        result = curr_collection.find_one({"id": author_id}, {'_id': 0})
        return {'Query Result': [result]}, 200

    def put(self):
        """
        Update a exist author document using json in request body
        :return: success response or error message
        """
        author_id = web_api_utility.check_valid_id(connected_database, self.collection_name)
        web_api_utility.check_json_content_type()
        data = request.get_json()
        data['id'] = author_id
        if not common_utility.check_valid_info_dict(data, self.collection_name):
            abort(400, error_message="Provided data is not in correct format")
        connected_database.update_data(data, self.collection_name)
        return {"Response": "Put success"}, 200

    def post(self):
        """
        Add 1 author document using json in request body
        :return: success response or error message
        """
        web_api_utility.check_json_content_type()
        data = request.get_json()
        if not common_utility.check_valid_info_dict(data, self.collection_name):
            abort(400, error_message="Provided data is not in correct format")
        connected_database.add_data(data, self.collection_name)
        return {"Response": "Post success"}, 200

    def delete(self):
        """
        Delete 1 author document using id
        :return: success response or error message
        """
        author_id = web_api_utility.check_valid_id(connected_database, self.collection_name)
        connected_database.delete_data(self.collection_name, author_id)
        return {"Response": "Delete success"}, 200


api.add_resource(Author, "/api/author")


class Scrape(Resource):
    """
    Resource class that handle "/api/scrape" request
    """
    required_args = ['book_count', 'author_count', 'start_url']
    b_scraper = book_scraper.BookScraper(connected_database)
    a_scraper = author_scraper.AuthorScraper(connected_database)

    def post(self):
        """
        Add documents to database using scraper
        :return: success response or error message
        """
        parsed_args = web_api_utility.check_valid_scrape_args(self.required_args)
        self.b_scraper.start(parsed_args[0], parsed_args[2])
        self.a_scraper.start(parsed_args[1], parsed_args[2])
        return {"Response": "Scrape success"}, 200


api.add_resource(Scrape, "/api/scrape")


@app.route('/api/books', methods=['POST'])
def post_multiple_books():
    """
    Add multiple book documents to database using json in request body
    :return: success response or error message
    """
    web_api_utility.check_json_content_type()
    data = request.get_json()
    if not isinstance(data, list):
        return {"Error_message": "Provided data is not in correct format"}, 400
    for info in data:
        if not common_utility.check_valid_info_dict(info, 'Book'):
            return {"Error_message": "Provided data is not in correct format"}, 400
    for info in data:
        connected_database.add_data(info, "Book")
    return {"Response": "Post success"}, 200


@app.route('/api/authors', methods=['POST'])
def post_multiple_authors():
    """
    Add multiple author documents to database using json in request body
    :return: success response or error message
    """
    web_api_utility.check_json_content_type()
    data = request.get_json()
    if not isinstance(data, list):
        return {"Error_message": "Provided data is not in correct format"}, 400
    for info in data:
        if not common_utility.check_valid_info_dict(info, 'Author'):
            return {"Error_message": "Provided data is not in correct format"}, 400
    for info in data:
        connected_database.add_data(info, "Author")
    return {"Response": "Post success"}, 200


@app.route('/api/search', methods=['GET'])
def search_database():
    """
    Query database using provided query string
    :return: query result or error message
    """
    is_valid, result = web_api_utility.check_valid_query_string()
    if not is_valid:
        return result, 400
    collection_name = result['collection_name']
    expression = result['expression']
    query_result = connected_database.database[collection_name].find(expression, {'_id': 0})
    result_list = []
    for result in query_result:
        result_list.append(result)
    return {'Query Result': result_list}, 200


@app.route('/api/top/book', methods=['GET'])
def top_k_book():
    """
    Get top k book information
    :return: query result or error message
    """
    is_valid, result = web_api_utility.check_valid_k_argument()
    if not is_valid:
        return result, 400
    k_arg = result['k_arg']
    all_book_doc = connected_database.database['Book'].find().sort([('rating', pymongo.DESCENDING)])
    book_count = 0
    result = []
    for book_doc in all_book_doc:
        if book_count == k_arg:
            break
        if 'title' in book_doc and 'rating' in book_doc:
            result.append({'name': book_doc['title'], 'rating': book_doc['rating']})
            book_count += 1
    return {'Query Result': result}, 200


@app.route('/api/top/author', methods=['GET'])
def top_k_author():
    """
    Get top k author information
    :return: query result or error message
    """
    is_valid, result = web_api_utility.check_valid_k_argument()
    if not is_valid:
        return result, 400
    k_arg = result['k_arg']
    all_author_doc = connected_database.database['Author'].find().sort([('rating', pymongo.DESCENDING)])
    author_count = 0
    result = []
    for author_doc in all_author_doc:
        if author_count == k_arg:
            break
        if 'author_name' in author_doc and 'rating' in author_doc:
            result.append({'name': author_doc['author_name'], 'rating': author_doc['rating']})
            author_count += 1
    return {'Query Result': result}, 200


if __name__ == "__main__":
    app.run(debug=True)
