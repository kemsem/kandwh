from flask import Flask, request, Response

from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage

bot_username = 'kanvaser_dwh'
bot_api_key = 'b8f254d2-507e-4ff4-ba35-db53aff7fadc'
bot_webhook = 'http://bookbus.000webhostapp.com/incoming'

app = Flask(__name__)
kik = KikApi(bot_username, bot_api_key)

kik.set_configuration(Configuration(webhook=bot_webhook))

@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, TextMessage):
            kik.send_messages([
                TextMessage(
                    to=message.from_user,
                    chat_id=message.chat_id,
                    body=message.body
                )
            ])

    return Response(status=200)


if __name__ == "__main__":
    app.run()