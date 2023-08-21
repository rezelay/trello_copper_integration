from flask import Flask, jsonify, request
from dotenv import load_dotenv

from webhooks import card_updated

load_dotenv()
app = Flask(__name__)


@app.route("/trello/webhooks", methods=['HEAD', 'POST'])
def trello_webhooks():
    try:
        if request.method == 'POST':
            webhook_data = request.json
            if request.json['action']['type'] == 'updateCard':
                new_card_data = card_updated(webhook_data)
                print(new_card_data)

                return jsonify(new_card_data), 200
        else:
            return jsonify({'message': 'Webhook registered with success'}), 200
    except EnvironmentError as err:
        return jsonify({'message': str(err)}), 500
    except AttributeError as err:
        print(str(err))
        # Here we respond as HTTP OK to not trigger any retries on Trello
        return jsonify({'message': str(err)}), 200
