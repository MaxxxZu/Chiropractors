import requests
from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import ProxyError, ConnectTimeout, ConnectionError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
CHROME_PATH = os.path.join(__location__, 'chromedriver')


class Request:
    def __init__(self, url, headers=None):
        self.headers = headers
        self.url = url
        self.proxy = self.get_proxies()
        self.cookies = self.get_cookies(self.url)

    def get_proxies(self):
        url = 'https://scrapingant.com/free-proxies/'
        proxies = set()
        options = Options()
        options.add_argument('headless')
        driver = webdriver.Chrome(executable_path=CHROME_PATH, options=options)
        driver.get(url)
        time.sleep(5)
        for i in driver.find_elements_by_xpath(
                    '//table[@class="proxies-table"]/tbody/tr')[1:51]:
            try:
                i.find_element_by_xpath('./td[3][contains(text(),"SOCKS5")]')
                proxy = ":".join([i.find_element_by_xpath('./td[1]').text,
                                  i.find_element_by_xpath('./td[2]').text])
            except NoSuchElementException:
                continue
            proxies.add(proxy)
        # return proxies
        driver.close()

        for proxy in proxies:
            try:
                proxies = {
                    'http': f"socks5://{proxy.split(':')[0]}:\
                                       {proxy.split(':')[1]}",
                    'https': f"socks5://{proxy.split(':')[0]}:\
                                        {proxy.split(':')[1]}"}
                response = requests.get('https://www.google.com',
                                        proxies=proxies, timeout=5,
                                        headers=self.headers)
                if response.raise_for_status():
                    return proxy
                    break
            except ProxyError:
                continue
            except TimeoutError:
                continue
            except ConnectTimeout:
                continue
            except ConnectionError:
                continue

    def get_cookies(self, url):
        response = requests.get(url, headers=self.headers)
        return response.headers['Set-Cookie']


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17\
        (KHTML, like Gecko)  Chrome/24.0.1312.57 Safari/537.17'
    }
    print(Request('https://handsdownbetter.org/', headers).proxy)
