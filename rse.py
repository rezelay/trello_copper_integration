import re
from typing import Any

import yaml
from helpers import chomp


class RSE:

    @staticmethod
    def trello_title_parse(title: str) -> dict[str, str]:
        match = re.search(r"^(\d+).\s+COPPER\s+(\d+)\s+\|(.*)\|(.*)$", title)
        if match is None:
            raise AttributeError('Trello card title does not comply with pattern')

        groups = match.groups()
        return {
            'month_sequence_number': int(groups[0]),
            'proposal_number': int(groups[1]),
            'client_name': chomp(groups[2]),
            'proposal_name': chomp(groups[3])
        }

    @staticmethod
    def trello_description_parse(description: str) -> dict[str, Any]:
        try:
            description_data: dict = yaml.load(description, Loader=yaml.Loader)

            name = description_data.get('name')
            email = description_data.get('email')
            pipeline = description_data.get('pipeline') or 'RSE Consultoria'

            if name is None or email is None:
                raise AttributeError('Trello card description does not comply with pattern')

            custom_fields = {}
            for key, value in description_data.items():
                match = re.search(r"^custom_(.*)$", key)
                if match:
                    custom_fields[match.groups()[0]] = value

            return {
                'name': name,
                'email': email,
                'pipeline': pipeline,
                'custom': custom_fields
            }
        except yaml.parser.ParserError:
            raise AttributeError('Trello card description does not parse into YAML')
