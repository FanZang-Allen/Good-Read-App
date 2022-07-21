"""
Scraper test may take several seconds
Try at least 3 times for a test if it is failed since scraper may failed due to connection
"""
import time
from unittest import TestCase

import requests
from bs4 import BeautifulSoup

import author_scraper
import database


class TestAuthorScraper(TestCase):
    def test_scrape_author_id(self):
        """
        Test author id is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = author_scraper.AuthorScraper(connected_database)
        test_author_url = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
        test_scraper.author_info = {'author_url': test_author_url}
        html_text = requests.get('https://www.goodreads.com/author/show/45372.Robert_C_Martin').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_author_id()
        self.assertEqual('45372', test_scraper.author_info['id'])

    def test_scrape_author_name(self):
        """
        Test author name is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = author_scraper.AuthorScraper(connected_database)
        test_scraper.author_info = {}
        html_text = requests.get('https://www.goodreads.com/author/show/45372.Robert_C_Martin').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_author_name()
        self.assertEqual("Robert C. Martin",
                         test_scraper.author_info['author_name'])

    def test_scrape_author_rating(self):
        """
        Test author avg rating & rating count is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = author_scraper.AuthorScraper(connected_database)
        test_scraper.author_info = {}
        html_text = requests.get('https://www.goodreads.com/author/show/45372.Robert_C_Martin').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_author_rating()
        self.assertNotEqual('null', test_scraper.author_info['rating'])
        self.assertNotEqual('null', test_scraper.author_info['rating_count'])

    def test_scrape_author_review(self):
        """
        Test author review count is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = author_scraper.AuthorScraper(connected_database)
        test_scraper.author_info = {}
        html_text = requests.get('https://www.goodreads.com/author/show/45372.Robert_C_Martin').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_author_review()
        self.assertNotEqual('null', test_scraper.author_info['review_count'])

    def test_scrape_author_image(self):
        """
        Test author image is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = author_scraper.AuthorScraper(connected_database)
        test_scraper.author_info = {}
        html_text = requests.get('https://www.goodreads.com/author/show/45372.Robert_C_Martin').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_author_image()
        self.assertNotEqual('null', test_scraper.author_info['image_url'])

    def test_scrape_author_book(self):
        """
        Test author book list is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = author_scraper.AuthorScraper(connected_database)
        test_scraper.author_info = {}
        html_text = requests.get('https://www.goodreads.com/author/show/45372.Robert_C_Martin').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_author_book()
        self.assertNotEqual(0, len(test_scraper.author_info['author_books']))

    def test_scrape_related_author(self):
        """
         Test related author list is scraped and stored in dict
         Test add similar authors url to unprocessed author url queue
        """
        connected_database = database.DataBase()
        test_scraper = author_scraper.AuthorScraper(connected_database)
        test_scraper.author_info = {'author_name': "Robert C. Martin"}
        html_text = requests.get('https://www.goodreads.com/author/show/45372.Robert_C_Martin').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_related_authors()
        self.assertNotEqual(0, len(test_scraper.author_info['related_authors']))
        self.assertNotEqual(0, len(test_scraper.unprocessed_author_queue))
