"""
Scraper test may take several seconds
Try at least 3 times for a test if it is failed since scraper may failed due to connection
"""
import time
from unittest import TestCase

import requests
from bs4 import BeautifulSoup

import book_scraper
import database


class TestBookScraper(TestCase):
    def test_scrape_book_id(self):
        """
        Test book id is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = book_scraper.BookScraper(connected_database)
        test_book_url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        test_scraper.book_info = {'book_url': test_book_url}
        html_text = requests.get('https://www.goodreads.com/book/show/3735293-clean-code').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_book_id()
        self.assertEqual('3735293', test_scraper.book_info['id'])

    def test_scrape_book_title(self):
        """
        Test book tile is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = book_scraper.BookScraper(connected_database)
        test_scraper.book_info = {}
        html_text = requests.get('https://www.goodreads.com/book/show/3735293-clean-code').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_book_title()
        self.assertEqual("Clean Code: A Handbook of Agile Software Craftsmanship",
                         test_scraper.book_info['title'])

    def test_scrape_book_isbn(self):
        """
        Test book ISBN is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = book_scraper.BookScraper(connected_database)
        test_scraper.book_info = {}
        html_text = requests.get('https://www.goodreads.com/book/show/3735293-clean-code').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_book_isbn()
        self.assertEqual("0132350882", test_scraper.book_info['ISBN'])

    def test_scrape_book_author(self):
        """
        Test book author is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = book_scraper.BookScraper(connected_database)
        test_scraper.book_info = {}
        html_text = requests.get('https://www.goodreads.com/book/show/3735293-clean-code').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_book_author()
        self.assertEqual(["Robert C. Martin"], test_scraper.book_info['author'])
        self.assertEqual(["https://www.goodreads.com/author/show/45372.Robert_C_Martin"],
                         test_scraper.book_info['author_url'])

    def test_scrape_book_rating(self):
        """
        Test book avg rating & rating count is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = book_scraper.BookScraper(connected_database)
        test_scraper.book_info = {}
        html_text = requests.get('https://www.goodreads.com/book/show/3735293-clean-code').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_book_rating()
        self.assertNotEqual('null', test_scraper.book_info['rating'])
        self.assertNotEqual('null', test_scraper.book_info['rating_count'])

    def test_scrape_book_review(self):
        """
        Test book review count is scraped and stored in dict
        """
        connected_database = database.DataBase()
        test_scraper = book_scraper.BookScraper(connected_database)
        test_scraper.book_info = {}
        html_text = requests.get('https://www.goodreads.com/book/show/3735293-clean-code').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_book_review()
        self.assertNotEqual('null', test_scraper.book_info['review_count'])

    def test_scrape_similar_book(self):
        """
         Test similar book list is scraped and stored in dict
         Test add similar books url to unprocessed book url queue
        """
        connected_database = database.DataBase()
        test_scraper = book_scraper.BookScraper(connected_database)
        test_book_url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        test_scraper.book_info = {'book_url': test_book_url}
        html_text = requests.get('https://www.goodreads.com/book/show/3735293-clean-code').text
        time.sleep(1)
        test_scraper.parsed_html = BeautifulSoup(html_text, 'lxml')
        test_scraper.scrape_similar_book()
        self.assertNotEqual(0, len(test_scraper.book_info['similar_books']))
        self.assertNotEqual(0, len(test_scraper.unprocessed_book_queue))
