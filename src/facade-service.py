from flask import Flask, request
from requests import get, post
from random import choice
import uuid

app = Flask(__name__)


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    log_url = ('http://localhost:8082/logging', 'http://localhost:8083/logging', 'http://localhost:8084/logging')
    if request.method == 'GET':
        message_url = 'http://localhost:8081/messages'

        response_log = get(choice(log_url)).text
        response_message = get(message_url).text
        return 'Messages-service reply: ' + response_message + '\n' \
               + 'Logging-service reply: ' + response_log + '\n'
    if request.method == 'POST':
        message = request.get_data()
        message_uuid = str(uuid.uuid4())

        return post(choice(log_url), data={"id": message_uuid, "msg": message}).text


if __name__ == '__main__':
    app.run(port=8080)
