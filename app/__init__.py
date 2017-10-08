import os
# import socket
import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask('foxApp')

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
    username = db.Column(db.String(80))
    score = db.Column(db.String(80))
    message = db.Column(db.String(80))

    def __init__(self, username, score, message):
        self.username = username
        self.score = score
        self.message = message

    def __repr__(self):
        return 'Message {}: {} - "{}">'.format(self.id, self.username, self.score)

    def as_dict(self):
        asDict = {
                  'username': self.username,
                  'score': self.score,
                  'message': self.message,
                  }
        return asDict


# ==============================================================================
# dummy api
# ==============================================================================
@app.route("/")
def index():
    return 'Hello from FLASK, my hostname is secret'
    # return 'Hello from FLASK, my hostname is: %s \n' % (socket.gethostname())

# http://localhost:5000/


# ==============================================================================
# messages api
# ==============================================================================

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return flask.jsonify([m.as_dict() for m in messages])


@app.route('/messages', methods=['POST'])
def post_messages():
    if not flask.request.is_json:
        flask.abort(400)

    # print(request.get_json())
    json = flask.request.get_json()

    if ('username' not in json) or ('score' not in json) or ('message' not in json):
        flask.abort(400)

    message = Message(username=json['username'],
                      score=json['score'],
                      message=json['message'])
    db.session.add(message)
    db.session.commit()

    return ''
