from flask import Flask
import sys
import hazelcast

app = Flask(__name__)

client = hazelcast.HazelcastClient(cluster_members=['127.0.0.1:5701', '127.0.0.1:5702', '127.0.0.1:5703'])
msg_q = client.get_queue('message-queue').blocking()
msg_data = []


@app.route('/messages', methods=['GET', 'POST'])
def messages_requests():
    while not msg_q.is_empty():
        msg_data.append(msg_q.take())
        print(f'Message: {msg_data[-1]}')
    return ', '.join(msg_data)


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
