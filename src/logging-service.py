import sys
from flask import Flask, request
import hazelcast

app = Flask(__name__)
client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"])
message_dict = client.get_map('log-map').blocking()


@app.route('/logging', methods=['GET', 'POST'])
def logging_requests():
    if request.method == 'GET':
        return ', '.join(message_dict.values())
    if request.method == 'POST':
        uuid = request.form['id']
        msg = request.form['msg']
        print(f'ID: {uuid}\nMessage: {msg}')
        message_dict.lock(uuid)
        try:
            message_dict.put(uuid, msg)
        finally:
            message_dict.unlock(uuid)
        return 'return_str'


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
