from flask import Flask, request
from requests import get, post
from random import choice
import sys
import uuid
import hazelcast
import consul

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('facade-service', port=int(sys.argv[1]), service_id=f"f{str(uuid.uuid4())}")
services = session.agent.services()

app = Flask(__name__)

log_clients = []
msg_clients = []
for key in services:
    link_pref = 'http://localhost:' + str(services[key]['Port']) + '/'
    if key[0] == 'l':
        log_clients.append(link_pref + 'logging')
    elif key[0] == 'm':
        msg_clients.append(link_pref + 'messages')

client = hazelcast.HazelcastClient(cluster_members=session.kv.get('hazel-ports')[1]['Value'].decode("utf-8").split())
msq_q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':
        response_log = get(choice(log_clients)).text
        response_msg = get(choice(msg_clients)).text
        return 'Messages-service reply: ' + response_msg + '\n' \
               + 'Logging-service reply: ' + response_log + '\n'
    if request.method == 'POST':
        message = request.get_json()
        msq_q.put(str(message))
        msg_uuid = str(uuid.uuid4())

        return post(choice(log_clients), data={"id": msg_uuid, "msg": message}).text


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
