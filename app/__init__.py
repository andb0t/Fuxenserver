import os
import socket
from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask('foxApp')

# ==============================================================================
# configure frontend for interaction
# ==============================================================================
# select the database backend and where to find it
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# suppress warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create db connection
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80))
    username = db.Column(db.String(80))

    def __init__(self, username, message):
        self.username = username
        self.message = message

    def __repr__(self):
        return 'Message {}: {} - "{}">'.format(self.id, self.username, self.message)

    def as_dict(self):
        return {
            'username': self.username,
            'message': self.message
        }


# ==============================================================================
# dummy api
# ==============================================================================
@app.route("/")
def index():
    return 'Hello from FLASK, my hostname is: %s \n' % (socket.gethostname())

# http://localhost:5000/


# ==============================================================================
# messages api
# ==============================================================================

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([m.as_dict() for m in messages])


@app.route('/messages', methods=['POST'])
def post_messages():
    if not request.is_json:
        abort(400)

    # print(request.get_json())
    json = request.get_json()

    if ('username' not in json) or ('message' not in json):
        abort(400)

    message = Message(username=json['username'], message=json['message'])
    db.session.add(message)
    db.session.commit()

    return ''
