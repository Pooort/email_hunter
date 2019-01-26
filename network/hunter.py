import requests

from settings import HUNTERAPIKEY


class HunterManager:

    @staticmethod
    def get_domain_data(domain):
        url = 'https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}'
        response = requests.get(url.format(domain=domain, api_key=HUNTERAPIKEY))
        return response.json()

