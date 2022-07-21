"""This file is part of Good Read Web Scraper

BookScraper class contains all the book information scraping functions.
Scraped data is stored in the connected mongodb database in DataBase Class.
"""
import time
import string
from collections import deque
import requests
from bs4 import BeautifulSoup
import database


class BookScraper:
    def __init__(self, connected_database: database.DataBase):
        """
        Class constructor that initialize all instance variables for web scraping
        :param connected_database: Mongodb cloud database connected in database.py
        """
        self.connected_database = connected_database
        self.book_info_list = []                # Store all the scraped book info dict
        self.processed_book_dict = {}           # Store all processed book url
        self.unprocessed_book_queue = deque()   # Store all unprocessed book url
        self.parsed_html = None                 # Current book page html
        self.book_info = None                   # Current processed book info dict

    def start(self, book_count: int, start_url: string):
        """
        The main function that control the scrape process, print success message if finished
        :param book_count: required number of books
        :param start_url: start url to scrape which is required to be a book page
        :return: None
        """
        if len(self.book_info_list) >= book_count:
            return
        if book_count > 200:
            print("Alert: Scraping book more than 200 is not allowed")
            return
        self.unprocessed_book_queue.clear()
        self.scrape_book(start_url)
        while True:
            time.sleep(2)
            if len(self.book_info_list) >= book_count:
                print('Book Scrape Success')
                break
            if len(self.unprocessed_book_queue) == 0:
                print('Similar book not enough')
                break
            next_book_url = self.unprocessed_book_queue.popleft()
            self.scrape_book(next_book_url)

    def scrape_book(self, url: string):
        """
        Scrape all book information based o book page url
        Call all other scrape function to add info to current book info dict
        Add dict to book_info_list after finishing scraping
        :param url: Good Read book page url
        :return: None
        """
        if url in self.processed_book_dict:
            return
        self.processed_book_dict[url] = True
        self.book_info = {'book_url': url}

        html_text = requests.get(url).text
        self.parsed_html = BeautifulSoup(html_text, 'lxml')

        self.scrape_book_id()
        self.scrape_book_title()
        self.scrape_book_isbn()
        self.scrape_book_author()
        self.scrape_book_rating()
        self.scrape_book_review()
        self.scrape_book_image()
        self.scrape_similar_book()

        self.book_info_list.append(self.book_info)
        self.connected_database.add_data(self.book_info, 'Book')

    def scrape_book_id(self):
        """
        Scrape book's id, print error message if failed.
        :return: None
        """
        try:
            book_url = self.book_info['book_url']
            book_id_end_index = 36
            for i in range(36, 1000):
                if not book_url[i].isnumeric():
                    book_id_end_index = i
                    break
            self.book_info['id'] = str(book_url[36: book_id_end_index])
        except (AttributeError, TypeError):
            print('Book ID Exception')

    def scrape_book_title(self):
        """
        Scrape book's title, print error message if failed.
        :return: None
        """
        try:
            book_title = self.parsed_html.find('h1', id='bookTitle').text.strip()
            self.book_info['title'] = book_title
        except (AttributeError, TypeError):
            print('Book Title Exception')

    def scrape_book_isbn(self):
        """
        Scrape book's ISBN, print error message if failed.
        :return: None
        """
        isbn = 'null'
        try:
            book_data_box = self.parsed_html.find('div', id='bookDataBox')
            clear_floats_list = book_data_box.find_all('div', class_='clearFloats')
            for info in clear_floats_list:
                if info.find('div', class_='infoBoxRowTitle').text.strip() == 'ISBN':
                    isbn = info.find('div', class_='infoBoxRowItem').text.strip().split()[0]
                    break
            self.book_info['ISBN'] = isbn
        except (AttributeError, TypeError):
            print('Book ISBN Exception')

    def scrape_book_author(self):
        """
        Scrape book's authors and their main page url, print error message if failed.
        :return: None
        """
        author_list = []
        author_url_list = []

        try:
            book_authors = self.parsed_html.find('div', id='bookAuthors')
            author_container_list = book_authors.find_all('div', class_='authorName__container')
            for info in author_container_list:
                author_url_list.append(info.a['href'])
                author_list.append(info.span.text)

        except (AttributeError, TypeError):
            author_list.clear()
            author_url_list.clear()
            print('Book Author Exception')

        self.book_info['author'] = author_list
        self.book_info['author_url'] = author_url_list

    def scrape_book_rating(self):
        """
        Scrape book's avg rating and rating count, print error message if failed.
        :return: None
        """
        try:
            book_meta = self.parsed_html.find('div', id='bookMeta')
            rating = book_meta.find('span', itemprop='ratingValue').text.strip()
            rating_count = book_meta.find('meta', itemprop='ratingCount')['content']
            self.book_info['rating'] = rating
            self.book_info['rating_count'] = rating_count
        except (AttributeError, TypeError):
            print('Book Rating Exception')

    def scrape_book_review(self):
        """
        Scrape book's review count, print error message if failed.
        :return: None
        """
        try:
            book_meta = self.parsed_html.find('div', id='bookMeta')
            review_count = book_meta.find('meta', itemprop='reviewCount')['content']
            self.book_info['review_count'] = review_count
        except (AttributeError, TypeError):
            print('Book Review Exception')

    def scrape_book_image(self):
        """
        Scrape book's image url, print error message if failed.
        :return: None
        """
        try:
            book_cover = self.parsed_html.find('div',
                                               id='imagecol').find('div', class_='bookCoverPrimary')
            image_url = book_cover.img['src']
            self.book_info['image_url'] = image_url
        except (AttributeError, TypeError):
            print('Book Image Exception')

    def scrape_similar_book(self):
        """
        Scrape book's related books, print error message if failed.
        Add related book url to unprocessed book queue to continue scraping
        :return: None
        """
        similar_book_name_list = []
        try:
            similar_book_link = self.parsed_html.find('a',
                                                      class_='actionLink right seeMoreLink')['href']
            time.sleep(2)
            similar_book_html_text = requests.get(similar_book_link).text
            parsed_similar_book_html = BeautifulSoup(similar_book_html_text, 'lxml')
            book_list = parsed_similar_book_html.find_all('div', class_='listWithDividers__item')

            for book in book_list:
                book_name = book.find('a',
                                      class_='gr-h3 gr-h3--serif gr-h3--noMargin').span.text.strip()
                book_url = 'https://www.goodreads.com' \
                           + book.find('a',class_='gr-h3 gr-h3--serif gr-h3--noMargin')['href']
                if book_url != self.book_info['book_url']:
                    similar_book_name_list.append(book_name)
                if book_url not in self.processed_book_dict:
                    # Add unseen book url to queue
                    self.unprocessed_book_queue.append(book_url)
        except (AttributeError, TypeError):
            similar_book_name_list.clear()
            print('Similar Book Name Exception')

        self.book_info['similar_books'] = similar_book_name_list
