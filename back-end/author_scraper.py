"""This file is part of Good Read Web Scraper

AuthorScraper class contains all the author information scraping functions.
Scraped data is stored in the connected mongodb database in DataBase Class.
"""
import time
import string
from collections import deque
import requests
from bs4 import BeautifulSoup
import database


class AuthorScraper:
    def __init__(self, connected_database: database.DataBase):
        """
        Class constructor that initialize all instance variables for web scraping
        :param connected_database: Mongodb cloud database connected in database.py
        """
        self.connected_database = connected_database
        self.author_info_list = []                   # Store all the scraped author info dict
        self.processed_author_dict = {}              # Store all processed author url
        self.unprocessed_author_queue = deque()      # Store all unprocessed author url
        self.parsed_html = None                      # Current author page html
        self.author_info = None                      # Current processed author info dict

    def start(self, author_count: int, start_book_url: string):
        """
        The main function that get the start author url and control the scrape process
        :param author_count: required number of authors
        :param start_book_url: start url to scrape which is required to be a book page
        :return: None
        """
        if len(self.author_info_list) >= author_count:
            return
        if author_count > 50:
            print("Alert: Scraping author more than 50 is not allowed")
            return

        book_html_text = requests.get(start_book_url).text
        book_parsed_html = BeautifulSoup(book_html_text, 'lxml')
        start_author_url = book_parsed_html.find('a', class_='authorName', itemprop='url')['href']

        self.unprocessed_author_queue.clear()
        self.scrape_author(start_author_url)
        while True:
            time.sleep(2)
            if len(self.author_info_list) >= author_count:
                print('Author Scrape Success')
                break
            if len(self.unprocessed_author_queue) == 0:
                print('Similar book not enough')
                break
            next_author_url = self.unprocessed_author_queue.popleft()
            self.scrape_author(next_author_url)

    def scrape_author(self, url: string):
        """
        Scrape all author information based on author page url
        Call all other scrape function to add info to current author info dict
        Add dict to author_info_list after finishing scraping
        :param url: Good Read author page url
        :return: None
        """
        if url in self.processed_author_dict:
            return
        self.processed_author_dict[url] = True
        self.author_info = {'author_url': url}

        html_text = requests.get(url).text
        self.parsed_html = BeautifulSoup(html_text, 'lxml')

        self.scrape_author_id()
        self.scrape_author_name()
        self.scrape_author_rating()
        self.scrape_author_review()
        self.scrape_author_image()
        self.scrape_author_book()
        self.scrape_related_authors()

        self.author_info_list.append(self.author_info)
        self.connected_database.add_data(self.author_info, 'Author')

    def scrape_author_id(self):
        """
        Scrape author's id, print error message if failed.
        :return: None
        """
        try:
            author_url = self.author_info['author_url']
            author_id_end_index = 38
            for i in range(38, 1000):
                if not author_url[i].isnumeric():
                    author_id_end_index = i
                    break
            self.author_info['id'] = str(author_url[38: author_id_end_index])
        except (AttributeError, TypeError):
            print('Author ID Exception')

    def scrape_author_name(self):
        """
        Scrape author's name, print error message if failed.
        :return: None
        """
        try:
            right_container = self.parsed_html.find('div', class_='rightContainer')
            author_name = right_container.find('h1', class_='authorName').span.text.strip()
            self.author_info['author_name'] = author_name
        except (AttributeError, TypeError):
            print('Author Name Exception')

    def scrape_author_rating(self):
        """
        Scrape author's rating, rating count, print error message if failed.
        :return: None
        """
        try:
            aggregate_info = self.parsed_html.find('div', itemprop='aggregateRating')
            rating = aggregate_info.find('span', itemprop='ratingValue').text.strip()
            rating_count = aggregate_info.find('span', itemprop='ratingCount')['content']
            self.author_info['rating'] = rating
            self.author_info['rating_count'] = rating_count
        except (AttributeError, TypeError):
            print('Author Rating Exception')

    def scrape_author_review(self):
        """
        Scrape author's review count, print error message if failed.
        :return: None
        """
        try:
            aggregate_info = self.parsed_html.find('div', itemprop='aggregateRating')
            review_count = aggregate_info.find('span', itemprop='reviewCount')['content']
            self.author_info['review_count'] = review_count
        except (AttributeError, TypeError):
            print('Author Review Exception')

    def scrape_author_image(self):
        """
        Scrape author's image url, print error message if failed.
        :return: None
        """
        try:
            author_container = self.parsed_html.find('div',
                                                     class_='leftContainer authorLeftContainer')
            image_url = author_container.find('img', itemprop='image')['src']
            self.author_info['image_url'] = image_url
        except (AttributeError, TypeError):
            print('Author Review Exception')

    def scrape_author_book(self):
        """
        Scrape author's book name list, print error message if failed.
        :return: None
        """
        author_book_list = []
        try:
            big_box_body = self.parsed_html.find('div', itemtype='https://schema.org/Collection')
            more_book_link = 'https://www.goodreads.com' + \
                             big_box_body.find('a', class_='actionLink')['href']

            time.sleep(2)
            more_book_html_text = requests.get(more_book_link).text
            more_book_parsed_html = BeautifulSoup(more_book_html_text, 'lxml')
            book_list = more_book_parsed_html.find_all('tr', itemtype='http://schema.org/Book')

            for book in book_list:
                book_name = book.find('span', itemprop='name').text.strip()
                author_book_list.append(book_name)

        except (AttributeError, TypeError):
            author_book_list.clear()
            print('Author Books Exception')

        self.author_info['author_books'] = author_book_list

    def scrape_related_authors(self):
        """
        Scrape author's related author, print error message if failed.
        Add related author url to unprocessed author queue to continue scraping
        :return: None
        """
        related_authors_list = []
        try:
            aggregate_info = self.parsed_html.find('div', itemprop='aggregateRating')
            similar_author_link = 'https://www.goodreads.com' \
                                  + aggregate_info.find_all('a')[-1]['href']

            time.sleep(2)
            similar_author_html_text = requests.get(similar_author_link).text
            similar_author_parsed_html = BeautifulSoup(similar_author_html_text, 'lxml')
            author_col = similar_author_parsed_html.find('div', class_='gr-col-md-8')
            author_list = author_col.find_all('span', itemprop='name')

            for author in author_list:
                author_name = author.text.strip()
                author_url = author.parent['href']
                if author_name != self.author_info['author_name']:
                    related_authors_list.append(author_name)
                if author_url not in self.processed_author_dict:
                    # Add unseen author url to queue
                    self.unprocessed_author_queue.append(author_url)

        except (AttributeError, TypeError):
            related_authors_list.clear()
            print('Related Author Exception')

        self.author_info['related_authors'] = related_authors_list
