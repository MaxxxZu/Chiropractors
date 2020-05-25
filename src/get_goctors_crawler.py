import os
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from models import City, session
import random

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.page_links = []

    def _get_web_driver(self, CHROME_PATH, headless=False):
        ua = UserAgent()
        userAgent = ua.random
        options = Options()
        if headless:
            options.add_argument('headless')
        options.add_argument('user-agent={0}'.format(userAgent))
        driver = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
        return driver

    def get_cities(self):
        cities_query = session.query(City).all()
        return random.choices(cities_query, k=10)

if __name__ == "__main__":
    START_URL = 'https://handsdownbetter.org/find-a-doctor/'
    url = 'https://handsdownbetter.org/find-a-doctor/?loc=Lorena&radius=75&submit=Search&terms=on'
    CHROME_PATH = os.path.join(__location__, 'chromedriver')
    OUTPUT_LOCATION = os.path.join(__location__, 'markets.xlsx')
    crawler = Crawler(START_URL)
    driver = crawler._get_web_driver(CHROME_PATH, headless=True)
    cities = crawler.get_cities()
    print([city.city_name for city in cities])
