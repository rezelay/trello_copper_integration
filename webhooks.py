from rse import RSE
from trello.client import Trello
from copper.client import Copper


def card_updated(webhook_data):
    trello_client = Trello('https://api.trello.com/1')
    copper_client = Copper('https://api.copper.com/developer_api/v1')

    modified_card_id = webhook_data['action']['data']['card']['id']
    card_data = trello_client.get_card(modified_card_id)
    title_parse = RSE.trello_title_parse(card_data['name'])
    description_parse = RSE.trello_description_parse(card_data['desc'])

    pipelines = copper_client.get_pipelines()
    pipeline = Copper.get_pipeline_from_name(pipelines, description_parse['pipeline'])
    stage = pipeline['stages'][0]
    contact = copper_client.get_or_create_person_by_email(description_parse['name'], description_parse['email'])

    field_definitions = copper_client.get_custom_field_definitions()
    fields_in_use = list(filter(
        lambda x: x['data_type'] == 'Dropdown' and x['name'] in description_parse['custom'].keys(),
        field_definitions
    ))

    custom_fields = []
    for key, value in description_parse['custom'].items():
        field_in_use = list(filter(lambda x: x['name'] == key, fields_in_use))[0]
        value_in_use = list(filter(lambda x: x['name'] == value, field_in_use['options']))[0]
        custom_fields.append((field_in_use['id'], value_in_use['id']))

    copper_client.create_opportunity(
        "RSE {0} | {1} | {2}".format(title_parse['proposal_number'], title_parse['client_name'],
                                     title_parse['proposal_name']),
        pipeline['id'],
        stage['id'],
        contact['id'],
        list(map(lambda x: {'custom_field_definition_id': x[0], 'value': x[1]}, custom_fields))
    )

    return trello_client.update_card(
        modified_card_id,
        {'name': "{0}. RSE {1} | {2} | {3}".format(
            title_parse['month_sequence_number'],
            title_parse['proposal_number'],
            title_parse['client_name'],
            title_parse['proposal_name']
        )}
    )
