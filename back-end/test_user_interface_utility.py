"""
Unit test file for user_interface_utility.py
"""
from unittest import TestCase
import user_interface_utility


class TestUIUtility(TestCase):
    def test_check_valid_input(self):
        """
        Test function identify if input str is in valid list
        """
        valid_list = ['one', 'two']
        self.assertTrue(user_interface_utility.check_valid_input('one', valid_list))
        self.assertTrue(user_interface_utility.check_valid_input('two', valid_list))
        self.assertFalse(user_interface_utility.check_valid_input('three', valid_list))

    def test_check_valid_export_path(self):
        """
        Test function identify if file path is valid to export json content
        """
        valid_export_path = 'json_file/valid_load_example.json'
        self.assertTrue(user_interface_utility.check_valid_export_path(valid_export_path))
        self.assertFalse(user_interface_utility.check_valid_export_path('file_not_exist'))
        self.assertFalse(user_interface_utility.check_valid_export_path('file_not_end_with_json'))
