from flask import Flask

app = Flask(__name__)


@app.route('/messages', methods=['GET', 'POST'])
def messages_requests():
    return 'Not implemented yet'


if __name__ == '__main__':
    app.run(port=8082)
