# This script was created by Kinga Kowalska.
# It is designed to scrape book data from my Read library at lubimyczytac.pl, Polish website for rating and reviewing books.
# For any questions or comments you may reach me at kinga_kowalska@onet.eu.

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

library_url = 'https://lubimyczytac.pl/profil/25810/kinga/biblioteczka/lista'
number_of_pages = 29
print('Gathering book data, please wait...')

# Creating file books.csv with headers.

with open('books.csv', 'w', encoding='utf-8') as f:
    f.writelines('Title,Author,Publisher,Date Read,Rating,My Rating,Category,Pages\n')
    f.close()

# Opening the lubimyczytac.pl Read library to scrape data from multiple pages.

driver = webdriver.Chrome()

def open_library(library_url):
    driver.get(library_url)
    time.sleep(2)
    accept_cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    accept_cookies.click()
    time.sleep(1)
    close_footer = driver.find_element(By.CSS_SELECTOR, 'body > div.js-footer-fixed.footer__fixed.w-100.pb-3.show > div > a > span')
    close_footer.click()
    choose_read = driver.find_element(By.CSS_SELECTOR, '#filtr > div > div.filtr__list--cats.filtr__list__library--cats > div > ul > li:nth-child(2) > label > div.filtr__itemTitle')
    choose_read.click()
    time.sleep(1)

open_library(library_url)

# Scraping book card data and saving it to the books.csv file.

for i in range(number_of_pages):
    def book_card():
        next_page = driver.find_element(By.CSS_SELECTOR, '#buttonPaginationListP > li.page-item.next-page > a')
        next_page.click()
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, 'lxml')
        books = soup.find_all('div', class_ = "authorAllBooks__single")
        with open('books.csv', 'a', encoding='utf-8') as f:
            for book in books:
                try:
                    title = book.find('a', class_ = "authorAllBooks__singleTextTitle float-left").text.strip()
                    title = '"' + title + '"'
                except AttributeError:
                    title = ''
                try:
                    author = book.find('div',  class_ = "authorAllBooks__singleTextAuthor authorAllBooks__singleTextAuthor--bottomMore").text.strip()
                    author = author.replace(',', ' |')
                except AttributeError:
                    author = ''
                try:
                    date_read = book.find('div', class_ = "small grey mt-2 mb-1 mb-md-0").text.strip()
                except AttributeError:
                    date_read = ''
                ratings = list(book.find_all('div', class_ = "listLibrary__ratingStars"))
                try:
                    rating = ratings[0].text.strip()
                    rating = rating.replace(',', '.')
                except IndexError:
                    rating = ''
                except AttributeError:
                    rating = ''
                try:
                    my_rating = ratings[1].text.strip()
                except IndexError:
                    my_rating = ''
                book_url = 'https://lubimyczytac.pl' + book.form['action']
                book_info = requests.get(book_url).text
                book_soup = BeautifulSoup(book_info, 'lxml')
                try:
                    publisher = book_soup.find('span', class_ = "book__txt d-block d-xs-none mt-2").text.strip()
                except AttributeError:
                    publisher = ''
                try:
                    category = book_soup.find('a', class_ = "book__category d-sm-block d-none").text.strip()
                    category = category.replace(',', ' |')
                except AttributeError:
                    category = ''
                try:
                    pages = book_soup.find('span', class_ = "d-sm-inline-block book-pages book__pages pr-2 mr-2 pr-sm-3 mr-sm-3").text.strip()
                except AttributeError:
                    pages = ''
                f.writelines(f'{title},{author},{publisher[12:].strip()},{date_read[12:].strip()},{rating[:3].strip()},{my_rating[:2].strip()},{category},{pages[0:3].strip()}\n')
            f.close()
        time.sleep(2)
    book_card()
    i = i + 1
    print(f'Gathered data from page {i}.')
driver.close()
print('Successfully gathered book data from all pages. Check file book.csv for the information.')