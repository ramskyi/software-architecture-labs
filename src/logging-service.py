import sys
from flask import Flask, request
import uuid
import hazelcast
import consul

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('logging-service', port=int(sys.argv[1]), service_id='l'+str(uuid.uuid4()))

app = Flask(__name__)
client = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701', '127.0.0.1:5702', '127.0.0.1:5703'])
msg_dict = client.get_map(session.kv.get('map')[1]['Value'].decode("utf-8")).blocking()


@app.route('/logging', methods=['GET', 'POST'])
def logging_requests():
    if request.method == 'GET':
        return ', '.join(msg_dict.values())
    if request.method == 'POST':
        uuid = request.form['id']
        msg = request.form['msg']
        print(f'ID: {uuid}\nMessage: {msg}')
        msg_dict.lock(uuid)
        try:
            msg_dict.put(uuid, msg)
        finally:
            msg_dict.unlock(uuid)
        return 'return_str'


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
