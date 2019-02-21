import itertools
import string
import time
import json

import requests

from time import sleep
from bs4 import BeautifulSoup
from helpers import get_web_driver, wait_function
from repo.location import LocationRepo
from settings import COMPANYTYPE

class AngelManager:

    driver = get_web_driver(headless=False)

    boundaries = []

    @classmethod
    def get_locations(cls):
        for items in itertools.combinations(string.ascii_lowercase, 2):
            cls.driver.get('https://angel.co/autocomplete/new_tags?query={}&tag_type=LocationTag&new_taggable_id=&new_taggable_type=&new_taggable_field=&exclude_new_places=true'.format(''.join(items)))
            yield AngelManager.parse_locations(cls.driver.page_source)

    @staticmethod
    def parse_locations(data):
        soup = BeautifulSoup(data, 'html.parser')
        locations_json = json.loads(soup.find("body").text)
        return locations_json


    @classmethod
    def get_companies_data_by_location(cls):
        for location in LocationRepo.get_all():
            cls.driver.get(
                'https://angel.co/companies?company_types[]=Startup&raised[min]=0&raised[max]=0&locations[]={}-{}'.format(location.location_id, location.display_name.replace(' ', '+')))
            companies_count = int(cls.driver.find_element_by_xpath(
                '//*[@id="root"]/div[5]/div[2]/div/div[2]/div[2]/div[1]/div[1]').text.split(' ')[
                                      0].replace(',', ''))

            if companies_count == 0:
                continue

            @wait_function
            def wait_companies():
                cls.driver.find_element_by_xpath('//div[@class="base startup"]')
            try:
                wait_companies()
            except:
                continue
            while True:
                try:
                    wait_button = cls.driver.find_element_by_xpath('//div[@class="more"]')
                    wait_button.click()
                    sleep(1)
                except:
                    break
                SCROLL_PAUSE_TIME = 0.5

                # Get scroll height
                last_height = cls.driver.execute_script("return document.body.scrollHeight")

                while True:
                    # Scroll down to bottom
                    cls.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)

                    # Calculate new scroll height and compare with last scroll height
                    new_height = cls.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
            companies_data = AngelManager.parse_companids_data(cls.driver.page_source)
            yield companies_data

    @classmethod
    def get_companies_data_by_price(cls, raised_min=1, raised_max=100000000):
        cls.driver.get('https://angel.co/companies?company_types[]=Startup&raised[min]={}&raised[max]={}'.format(raised_min, raised_max))
        companies_count = int(cls.driver.find_element_by_xpath('//*[@id="root"]/div[5]/div[2]/div/div[2]/div[2]/div[1]/div[1]').text.split(' ')[0].replace(',', ''))
        if companies_count > 400 and raised_max != raised_min:
            boundery = raised_min + (raised_max - raised_min) // 2
            yield from cls.get_companies_data(raised_min, boundery)
            yield from cls.get_companies_data(boundery, raised_max)
        else:
            @wait_function
            def wait_companies():
                cls.driver.find_element_by_xpath('//div[@class="base startup"]')
            wait_companies()
            while True:
                try:
                    wait_button = cls.driver.find_element_by_xpath('//div[@class="more"]')
                    wait_button.click()
                    sleep(1)
                except:
                    break
                SCROLL_PAUSE_TIME = 0.5

                # Get scroll height
                last_height = cls.driver.execute_script("return document.body.scrollHeight")

                while True:
                    # Scroll down to bottom
                    cls.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)

                    # Calculate new scroll height and compare with last scroll height
                    new_height = cls.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
            companies_data = AngelManager.parse_companids_data(cls.driver.page_source)
            yield companies_data

    # @staticmethod
    # def get_companies_data(raised_min=0, raised_max=100000000):
    #     #url = 'https://angel.co/company_filters/search_data?filter_data%5Bcompany_types%5D%5B%5D={}&page={}&filter_data[raised][min]={}&filter_data[raised][max]={}&sort=signal'
    #     url = 'https://angel.co/company_filters/search_data'
    #     payload = {
    #         'filter_data[company_types][]': COMPANYTYPE,
    #         'filter_data[raised][min]': 10000,
    #         'filter_data[raised][max]': 6652299,
    #         'sort': 'signal'
    #     }
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    #         'referer': 'https://angel.co/companies?company_types[]=Startup&raised[min]=10000&raised[max]=6652299'
    #     }
    #     page = 1
    #     is_data_returned = True
    #     while is_data_returned:
    #         response = requests.post(url.format(COMPANYTYPE, page, raised_min, raised_max), headers=headers, data=payload)
    #         sleep(1)
    #         json_response = response.json()
    #         if json_response.get('ids') is None:
    #             is_data_returned = False
    #         else:
    #             companies_data = AngelManager.get_companies_data_by_json(json_response)
    #             yield companies_data
    #         page += 1
    #         if page > 20:
    #             bound = int(raised_max/2)
    #             yield from AngelManager.get_companies_data(raised_min, bound)
    #             yield from AngelManager.get_companies_data(bound, raised_max)

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
##root > div.page.unmodified.dl85.layouts.fhr17.header._a._jm > div.companies.dc59.fix36._a._jm > div > div.content > div.dc59.frs86._a._jm > div.results > div:nth-child(2) > div > div.column.location > div.value > div > a
    @staticmethod
    def parse_companids_data(data):
        soup = BeautifulSoup(data, 'html.parser')
        companies_data = []
        for startup in soup.find_all("div", class_="base startup"):
            company_data = {
                'name': startup.select('div.name')[0].text.strip(),
                'location': startup.select('div.column.location > div.value')[0].text.strip(),
                'market': startup.select('div.column.market > div.value')[0].text.strip(),
                'website': startup.select('div.column.website > div.value')[0].text.strip(),
                'employees': startup.select('div.column.company_size > div.value')[0].text.strip(),
                'stage': startup.select('div.column.stage > div.value')[0].text.strip(),
                'total_raised': startup.select('div.raised > div.value')[0].text.strip()
            }
            if company_data['stage'] != 'Acquired' and company_data['website']:
                companies_data.append(company_data)
        return companies_data
