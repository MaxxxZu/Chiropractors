import csv
import json
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from models import State, City, session


class Request:

    def __init__(self, state):
        self.state = state

    def get_page_url(self):
        if self.state in ['California', 'Washington']:
            self.url = f'https://en.wikipedia.org/wiki/\
                         List_of_cities_and_towns_in_{self.state}'
        elif self.state in ['Illinois', 'Pennsylvania', 'Florida']:
            self.url = f'https://en.wikipedia.org/wiki/\
                         List_of_municipalities_in_{self.state}'
        else:
            self.url = 'https://en.wikipedia.org/wiki/List_of_cities_in_Texas'
        self.get_cities_page_source()

    def get_cities_page_source(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
                       AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/83.0.4103.61 Safari/537.36'
                        }
        self.response = requests.get(self.url, headers=self.headers)
        try:
            self.response.raise_for_status()
            self.soup = BeautifulSoup(self.response.text, "html.parser")
        except requests.HTTPError as error:
            print(error)


class Crawler:
    def __init__(self, state, soup):
        self.state = state
        self.cities = []
        if state in ['Washington', 'California', 'Florida', 'Texas']:
            self.content_table = soup.find_all('table')[1].tbody.find_all('tr')
        else:
            self.content_table = soup.find('table').tbody.find_all('tr')
        self.get_data()

    def get_data(self):
        for city in self.content_table:
            if city.find('a') and city.find('a')['href'].startswith('/wiki/'):
                self.cities.append(city.find('a').string)


class Output:
    def __init__(self, all_cities, method):
        self.all_cities = all_cities
        self.method = method

    def output_choice(self):
        if self.method == 'xls':
            self.to_xls()
        elif self.method == 'json':
            self.to_json()
        elif self.method == 'db':
            self.to_db()
        else:
            self.to_csv()

    def to_xls(self):
        print('to Xls')
        with xlsxwriter.Workbook('cities.xlsx') as workbook:
            worksheet = workbook.add_worksheet()
            list_for_xls = []
            for state, cities in self.all_cities.items():
                for city in cities:
                    list_for_xls.append([state, city])
            for row, value in enumerate(list_for_xls):
                for col, data in enumerate(value):
                    worksheet.write(row, col, data)

    def to_json(self):
        with open('cities.json', 'w') as file:
            dict_for_json = {}
            for state, cities in self.all_cities.items():
                dict_for_json[state] = [city for city in cities]
            json.dump(dict_for_json, file, indent=4, sort_keys=True)

    def to_db(self):
        for state in self.all_cities.keys():
            stat = session.query(State).filter_by(state=state).first()
            if not stat:
                session.add(State(state=state))
        session.commit()

    def to_csv(self):
        with open('cities.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for state, cities in self.all_cities.items():
                for city in cities:
                    row = [state, city]
                    writer.writerow(row)


if __name__ == "__main__":
    # states = ['Washington', 'California']
    all_cities = {}
    states = ['California', 'Texas', 'Illinois', 'Pennsylvania', 'Florida',
              'Washington', ]
    for state in states:
        source = Request(state)
        source.get_page_url()
        data = Crawler(source.state, source.soup)
        all_cities[data.state] = set(data.cities)
    Output(all_cities, 'db').output_choice()
