from flask import Flask
import sys
import hazelcast
import uuid
import consul

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('messages-service', port=int(sys.argv[1]), service_id='m'+str(uuid.uuid4()))

app = Flask(__name__)

client = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701', '127.0.0.1:5702', '127.0.0.1:5703'])
msg_q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()
msg_data = []


@app.route('/messages', methods=['GET', 'POST'])
def messages_requests():
    while not msg_q.is_empty():
        msg_data.append(msg_q.take())
        print(f'Message: {msg_data[-1]}')
    return ', '.join(msg_data)


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
