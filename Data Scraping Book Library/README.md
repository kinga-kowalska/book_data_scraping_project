# Data Scraping Book Library

This is a Python script that scrapes my Read Books library from Polish book review website lubimyczytac.pl.\
It gathers **Title**, **Author**, **Publisher**, **Date Read**, general **Rating**, **My Rating**, **Category** and number of **Pages** and saves in in **books.csv** file.

## Requirements

The script uses **Selenium**, **Requests** and **BeautifulSoup4** libraries.
It also requires **Google Chrome** and **chromedriver** to run Selenium.

## Method

Initially, the html source code of the webpage to parse data was retrieved only using the Requests library.
However, due to website constraints it was impossible to retrieve working urls for each consecutive page of the library, therefore Selenium was used to "manually" click through the pages and retrieve the source code.
