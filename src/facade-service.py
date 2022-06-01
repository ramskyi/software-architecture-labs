from flask import Flask, request
from requests import get, post
from random import choice
import uuid
import hazelcast

app = Flask(__name__)

log_url = ('http://localhost:8083/logging', 'http://localhost:8084/logging', 'http://localhost:8085/logging')
msg_url = ('http://localhost:8081/messages', 'http://localhost:8082/messages',)

client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"])
msq_q = client.get_queue("message-queue").blocking()


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':
        response_log = get(choice(log_url)).text
        response_msg = get(choice(msg_url)).text
        return 'Messages-service reply: ' + response_msg + '\n' \
               + 'Logging-service reply: ' + response_log + '\n'
    if request.method == 'POST':
        message = request.get_json()
        msq_q.put(str(message))
        msg_uuid = str(uuid.uuid4())

        return post(choice(log_url), data={"id": msg_uuid, "msg": message}).text


if __name__ == '__main__':
    app.run(port=8080)
