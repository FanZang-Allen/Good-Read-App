"""
Unit test file for query_parser.py
"""
from unittest import TestCase
from query_parser import parse_collection_name
from query_parser import parse_field
from query_parser import parse_query_string
import database


class TestQueryParser(TestCase):
    def test_dot_operator(self):
        """
        Test parser correctly get the collection name using dot operator
        """
        self.assertEqual('Book', parse_collection_name('book.id: 123'))
        self.assertEqual('Author', parse_collection_name('author.id: 123'))
        # string other than book/author is not allowed before dot operator
        self.assertEqual(None, parse_collection_name('test.id: 123'))

    def test_colon_operator(self):
        """
        Test parser correctly get the field using colon operator
        """
        self.assertEqual('id', parse_field('book.id: 123', 'Book'))
        self.assertEqual('rating', parse_field('author.rating: 123', 'Author'))
        # ISBN is not an attribute in author info dict
        self.assertEqual(None, parse_field('author.ISBN: 123', 'Author'))

    def test_quote_operator(self):
        """
        Test parser correctly generate expression with quote
        """
        connected_database = database.DataBase()
        connected_database.clear_collection('Book')
        connected_database.clear_collection('Author')
        connected_database.load_json_data('json_file/valid_load_example.json')
        # Test find exact document
        parsed_result = parse_query_string('author.rating: \"4.46\"')
        result = connected_database.database[parsed_result[0]].find_one(parsed_result[1])
        self.assertEqual('4.46', result['rating'])
        # quote is not allowed with comparison operator
        self.assertEqual(None, parse_query_string('author.id: > \"123\"'))

    def test_logic_operator(self):
        """
        Test parser correctly generate expression with logical operator
        """
        connected_database = database.DataBase()
        connected_database.clear_collection('Book')
        connected_database.clear_collection('Author')
        connected_database.load_json_data('json_file/valid_load_example.json')
        # Test AND
        and_example = 'author.rating: > 4.45 AND author.rating: < 4.47'
        and_result = parse_query_string(and_example)
        result = connected_database.database[and_result[0]].find_one(and_result[1])
        self.assertEqual('4.46', result['rating'])
        # Test OR
        or_example = 'author.id: > 4.23 OR author.rating: < 4.23'
        or_result = parse_query_string(or_example)
        result = connected_database.database[or_result[0]].find_one(or_result[1])
        self.assertNotEqual('4.23', result['rating'])
        # Test NOT
        not_result = parse_query_string('author.rating: NOT 4.22')
        result = connected_database.database[not_result[0]].find_one(not_result[1])
        self.assertNotEqual('4.22', result['rating'])

    def test_comparison_operator(self):
        """
        Test parser correctly generate expression with comparison operator
        """
        connected_database = database.DataBase()
        connected_database.clear_collection('Book')
        connected_database.clear_collection('Author')
        connected_database.load_json_data('json_file/valid_load_example.json')
        # Test greater
        greater_res = parse_query_string('author.rating: > 4.45')
        result = connected_database.database[greater_res[0]].find_one(greater_res[1])
        self.assertEqual('4.46', result['rating'])
        # Test smaller
        smaller_res = parse_query_string('author.rating: < 4.23')
        result = connected_database.database[smaller_res[0]].find_one(smaller_res[1])
        self.assertEqual('4.22', result['rating'])
        # Test NOT with comparison
        not_res = parse_query_string('author.rating: NOT > 4.22')
        result = connected_database.database[not_res[0]].find_one(not_res[1])
        self.assertEqual('4.22', result['rating'])
