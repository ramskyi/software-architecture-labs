from flask import Flask, request
from requests import get, post
import uuid

app = Flask(__name__)


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    log_url = 'http://localhost:8081/logging'
    if request.method == 'GET':
        message_url = 'http://localhost:8082/messages'
        return 'Messages-service reply: ' + get(message_url).content.decode('utf-8') + '\n' \
               + 'Logging-service reply: ' + get(log_url).content.decode('utf-8') + '\n'
    if request.method == 'POST':
        r = post(log_url, data={str(uuid.uuid4()): request.get_data()})
        return str(r.status_code) + '\n'


if __name__ == '__main__':
    app.run(port=8080)
