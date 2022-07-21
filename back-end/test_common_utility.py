"""
Unit test file for common_utility.py
"""
from unittest import TestCase
from common_utility import check_positive
from common_utility import check_valid_info_dict
from common_utility import check_valid_start_url
from common_utility import check_valid_json_file


class TestCommonUtility(TestCase):
    def test_check_positive(self):
        """
        Test function correctly identify positive float string
        """
        self.assertEqual(False, check_positive('Unable to be float'))
        self.assertEqual(False, check_positive('-1'))
        self.assertEqual(True, check_positive('1'))
        self.assertEqual(True, check_positive('01'))
        self.assertEqual(True, check_positive('1.0'))

    def test_check_valid_info_dict(self):
        """
        Test function correctly identify valid info dict
        """
        test_dict = {"normal_attribute": 'test',
                     "array_attribute": []}

        # Only Book or Author is allowed as the second input
        self.assertEqual(False, check_valid_info_dict(test_dict, 'Test'))

        # id should be inside the dict
        self.assertEqual(False, check_valid_info_dict(test_dict, 'Book'))
        test_dict['id'] = "34927404"
        self.assertEqual(True, check_valid_info_dict(test_dict, 'Book'))

        # All normal attribute inside dict should be a str
        test_dict['normal_attribute'] = 1
        self.assertEqual(False, check_valid_info_dict(test_dict, 'Book'))
        test_dict['normal_attribute'] = '1'

        # All array attribute inside dict should be an array of str
        test_dict['array_attribute'] = [1, 2, 3]
        self.assertEqual(False, check_valid_info_dict(test_dict, 'Book'))

        test_dict['array_attribute'] = ['1', '2']
        self.assertEqual(True, check_valid_info_dict(test_dict, 'Book'))

    def test_check_valid_start_url(self):
        """
        Test function correctly identify valid start book page
        """
        self.assertEqual(False, check_valid_start_url('https://www.goodreads.com/author'))
        self.assertEqual(True, check_valid_start_url('https://www.goodreads.com/book'))

    def test_check_valid_json_file(self):
        """
        Test function correctly identify valid json file
        """
        invalid_file_path = 'json_file/invalid_load_example.json'
        valid_file_path = 'json_file/valid_load_example.json'
        self.assertNotEqual(invalid_file_path, check_valid_json_file(invalid_file_path))
        self.assertEqual(valid_file_path, check_valid_json_file(valid_file_path))
