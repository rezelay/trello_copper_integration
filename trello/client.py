import json
import os

import requests


class Trello:

    def __init__(self, base_url):
        api_key = os.getenv('TRELLO_API_KEY')
        api_token = os.getenv('TRELLO_API_TOKEN')

        if api_key is None or api_token is None:
            raise EnvironmentError('Trello credentials not present in environment')

        self.base_url = base_url
        self.default_headers = {'Accept': 'application/json'}
        self.default_query = {'key': api_key, 'token': api_token}

    def get_card(self, card_id):
        response = requests.request(
            'GET',
            "{base_url}/cards/{id}".format(base_url=self.base_url, id=card_id),
            headers=self.default_headers,
            params=self.default_query
        )

        return json.loads(response.text)

    def update_card(self, card_id, attributes):
        response = requests.request(
            'PUT',
            "{base_url}/cards/{id}".format(base_url=self.base_url, id=card_id),
            headers=self.default_headers,
            params={**self.default_query, **attributes}
        )

        return json.loads(response.text)
