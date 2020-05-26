import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from database_out import DatabaseOutput

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.inner_pages_links = set()
        self.inner_page_info = []
        self.item_links = set()
        self.items = []

    def _get_web_driver(self, CHROME_PATH, headless=False):
        """
        Create a Webdriver
        """
        options = Options()
        if headless:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options,
                                       executable_path=CHROME_PATH)

    def check_page_link(self, url):
        """
        check if this page is what we need
        """
        try:
            self.driver.get(url)
            assert "No results found." not in self.driver.page_source
        except TimeoutException as error:
            print(url, error)

    def get_inner_pages_links(self):
        """
        collect links to the necessary internal pages
        Append links in to iinner_pages_links Set
        """
        url = self.start_url
        self.check_page_link(url)
        self.driver.get(url)
        self.inner_pages_links.add(self.start_url)

    def inner_page_parse(self, inner_url):
        """
        Recive internal pages url and
        collect info to the necessary internal pages
        """
        url = inner_url
        self.check_page_link(url)
        self.driver.get(url)
        time.sleep(2)
        try:
            element = self.driver.find_element_by_xpath(
                '//table[@class="wikitable sortable jquery-tablesorter"]/tbody'
                )
            for row in element.find_elements_by_xpath('./tr'):
                state_name = row.find_element_by_xpath('./td[1]').text
                state_abr = row.find_element_by_xpath('./td[2]').text
                capital_name = row.find_element_by_xpath('./td[4]').text
                item_link = row.find_element_by_xpath(
                                './td[1]/a').get_attribute('href')
                inner_page_info = [state_name, state_abr, capital_name]
                self.inner_page_info.append(inner_page_info)
                self.item_links.add(item_link)
        except NoSuchElementException:
            print('No such element')
        """
        pagination
        """

    def parse_item_page(self, item_url):
        """
        collect info for item
        """
        url = item_url
        self.check_page_link(url)
        self.driver.get(url)
        time.sleep(2)


def main():
    START_URL = 'https://en.wikipedia.org/wiki/\
                 List_of_capitals_in_the_United_States'
    CHROME_PATH = os.path.join(__location__, 'chromedriver')
    crawler = Crawler(START_URL)
    crawler._get_web_driver(CHROME_PATH, headless=True)
    crawler.get_inner_pages_links()
    for page_link in crawler.inner_pages_links:
        crawler.inner_page_parse(page_link)
        time.sleep(3)
    for item_link in crawler.item_links:
        print(item_link)
        time.sleep(1)
    DatabaseOutput(crawler.inner_page_info).states_capitals_out()


if __name__ == "__main__":
    main()
