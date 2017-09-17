import socket
from flask import Flask
from flask import abort
from flask import jsonify
from flask import request

app = Flask('foxApp')


# dummy api
@app.route("/")
def index():
    return 'Hello from FLASK, my hostname is: %s \n' % (socket.gethostname())

# http://localhost:5000/


# messages api
message_store = [{'username': 'test', 'message': 'A test message.'}]


@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(message_store)


@app.route('/messages', methods=['POST'])
def post_messages():
    global messages_store
    if not request.is_json:
        abort(400)

    # print(request.get_json())
    json = request.get_json()

    messages_store += [json]

    return ''
