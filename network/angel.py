import requests

from time import sleep
from bs4 import BeautifulSoup

from settings import COMPANYTYPE


class AngelManager:

    @staticmethod
    def get_companies_data():
        sort_types = ['joined', 'signal', 'raised']
        url = 'https://angel.co/company_filters/search_data?filter_data%5Bcompany_types%5D%5B%5D={}&page={}&sort={}'
        for sort_type in sort_types:
            page = 1
            is_data_returned = True
            while is_data_returned:
                response = requests.get(url.format(COMPANYTYPE, page, sort_type))
                sleep(1)
                json_response = response.json()
                if json_response.get('ids') is None:
                    is_data_returned = False
                else:
                    companies_data = AngelManager.get_companies_data_by_json(json_response)
                    yield companies_data
                page += 1

    @staticmethod
    def get_companies_data_by_json(json_data):
        url = 'https://angel.co/companies/startups'
        payload = {
            'ids[]': json_data['ids'],
            'hexdigest': json_data['hexdigest']
        }
        response = requests.get(url, params=payload)
        companies_data = AngelManager.parse_companids_data(response.json()['html'])
        return companies_data

    @staticmethod
    def parse_companids_data(data):
        soup = BeautifulSoup(data, 'html.parser')
        companies_data = []
        for startup in soup.find_all("div", class_="base startup"):
            company_data = {
                'name': startup.select('div.pitch')[0].text.strip(),
                'location': startup.select(' div.column.hidden_column.location > div.value')[0].text.strip(),
                'market': startup.select('div.column.hidden_column.market > div.value')[0].text.strip(),
                'website': startup.select('div.column.hidden_column.website > div.value')[0].text.strip(),
                'employees': startup.select('div.column.company_size.hidden_column > div.value')[0].text.strip(),
                'stage': startup.select('div.column.hidden_column.stage > div.value')[0].text.strip(),
                'total_raised': startup.select('div.column.hidden_column.raised > div.value')[0].text.strip()
            }
            if company_data['stage'] != 'Acquired' and company_data['website']:
                companies_data.append(company_data)
        return companies_data
