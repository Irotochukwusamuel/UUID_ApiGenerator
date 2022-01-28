import json

from flask import Flask, make_response, jsonify

from generator import Generator

app = Flask(__name__)
generate = Generator()


@app.route('/')
def index():
    response = make_response(json.dumps(generate.callback(), indent=4))  # dumping the returned data
    response.headers["Content-Type"] = 'application/json'
    return response


if __name__ == '__main__':
    app.run()
