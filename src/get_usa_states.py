"""
Задача. отпарсить содержимое всех страниц
1) Создаем драйвер
2) Берем стартовый линк и проверяем та ли эта страница, что нужно
3) если та, то собираем ссылки на нужные внутренние страницы
4) переходим на каждую внутреннюю страницу с учетом пагинации
5) собираем нужную информацию с этих страниц
6) переходим на конечные страницы
7) собираем нужную информацию с этих страниц
"""
import os
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from models import State

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.inner_pages_links = set()
        self.inner_page_info = []

    def _get_web_driver(self, CHROME_PATH, headless=False):
        """
        Create a Webdriver
        """
        ua = UserAgent()
        userAgent = ua.random
        options = Options()
        if headless:
            options.add_argument('headless')
        options.add_argument('user-agent={0}'.format(userAgent))
        driver = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
        return driver

    def get_start_page(self, driver):
        """
        check if this page is what we need
        """
        try:
            driver.get(self.start_url)
            assert driver.title.startswith('List of capitals'), 'False Page'
            time.sleep(2)
        except TimeoutException as error:
            print(self.start_url, error)

    def get_inner_pages_links(self, driver):
        """
        collect links to the necessary internal pages
        Append links in to iinner_pages_links Set
        """
        self.inner_pages_links.add(self.start_url)

    def inner_page_parse(self, driver, url):
        """
        Recive internal pages url and
        collect info to the necessary internal pages
        """
        driver.get(url)
        time.sleep(2)
        try:
            element = driver.find_element_by_xpath(
                '//table[@class="wikitable sortable jquery-tablesorter"]/tbody'
                )
            for row in element.find_elements_by_xpath('./tr'):
                state_name = row.find_element_by_xpath('./td[1]').text
                state_abr = row.find_element_by_xpath('./td[2]').text
                capital_name = row.find_element_by_xpath('./td[4]').text
                inner_page_info = [state_name, state_abr, capital_name]
                self.inner_page_info.append(inner_page_info)
        except NoSuchElementException:
            print('No such element')
        """
        pagination
        """


class Output:
    def __init__(self, values):
        self.values = values
        self.to_database()

    def to_database(self):
        for state_name, state_abr, capital_name in self.values:
            State().add_state(state_name, state_abr)
            state = State().get_state(state_name)
            state.add_state_capital(capital_name)


def main():
    START_URL = 'https://en.wikipedia.org/wiki/\
                 List_of_capitals_in_the_United_States'
    CHROME_PATH = os.path.join(__location__, 'chromedriver')
    crawler = Crawler(START_URL)
    driver = crawler._get_web_driver(CHROME_PATH, headless=True)
    crawler.get_start_page(driver)
    crawler.get_inner_pages_links(driver)
    for page_link in crawler.inner_pages_links:
        crawler.inner_page_parse(driver, page_link)
        time.sleep(3)
    Output(crawler.inner_page_info)


if __name__ == "__main__":
    main()
