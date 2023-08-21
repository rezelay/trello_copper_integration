import json
import os

import requests


class Copper:

    def __init__(self, base_url):
        api_key = os.getenv('COPPER_API_KEY')
        api_user_email = os.getenv('COPPER_API_USER_EMAIL')

        if api_key is None or api_user_email is None:
            raise EnvironmentError('Copper credentials not present in environment')

        self.base_url = base_url
        self.default_headers = {
            'Content-Type': 'application/json',
            'X-PW-Application': 'developer_api',
            'X-PW-AccessToken': api_key,
            'X-PW-UserEmail': api_user_email,
        }

    @staticmethod
    def get_pipeline_from_name(array: list[dict], name: str) -> dict:
        result = list(filter(lambda x: x['name'] == name, array))
        if len(result) == 0:
            raise AttributeError('Name \'{0}\' not found in array'.format(name))

        return result[0]

    def get_pipelines(self):
        response = requests.request(
            'GET',
            "{base_url}/pipelines".format(base_url=self.base_url),
            headers=self.default_headers
        )

        return json.loads(response.text)

    def get_custom_field_definitions(self):
        response = requests.request(
            'GET',
            "{base_url}/custom_field_definitions".format(base_url=self.base_url),
            headers=self.default_headers
        )

        return json.loads(response.text)

    def get_or_create_person_by_email(self, name: str, email: str) -> dict:
        response = requests.request(
            'POST',
            "{base_url}/people/fetch_by_email".format(base_url=self.base_url),
            headers=self.default_headers,
            params={'email': email}
        )

        if response.status_code == 200:
            return json.loads(response.text)

        response = requests.request(
            'POST',
            "{base_url}/people".format(base_url=self.base_url),
            headers=self.default_headers,
            data=json.dumps({'name': name, 'emails': [{'email': email, 'category': 'work'}]})
        )

        if response.status_code == 200:
            return json.loads(response.text)

        raise AttributeError('Could not create new person in Copper using: {0}'.format(email))

    def create_opportunity(self, name: str, pipeline_id: int, stage_id: str, contact_id: int, custom_fields: list[dict[str, int]]):
        response = requests.request(
            'POST',
            "{base_url}/opportunities".format(base_url=self.base_url),
            headers=self.default_headers,
            data=json.dumps({
                'name': name,
                'pipeline_id': pipeline_id,
                'stage_id': stage_id,
                'primary_contact_id': contact_id,
                'custom_fields': custom_fields
            })
        )

        if response.status_code == 200:
            return json.loads(response.text)

        raise AttributeError('Could not create new opportunity in Copper using: {0}'.format(name))
