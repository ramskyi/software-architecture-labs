from flask import Flask, request

app = Flask(__name__)
messages = {}


@app.route('/logging', methods=['GET', 'POST'])
def logging_requests():
    if request.method == 'GET':
        return str(list(messages.values()))
    if request.method == 'POST':
        key, value = request.form.to_dict().popitem()
        messages[key] = value
        return {'status_code': 200}


if __name__ == '__main__':
    app.run(port=8081)
