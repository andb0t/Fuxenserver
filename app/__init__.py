import datetime
import os
import flask
import flask_sqlalchemy

app = flask.Flask('foxApp')

# ==============================================================================
# configure frontend for interaction
# ==============================================================================
# select the database backend and where to find it
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# suppress warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create db connection
db = flask_sqlalchemy.SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    score = db.Column(db.Integer)
    message = db.Column(db.String(80))
    time = db.Column(db.String(80))

    def __init__(self, username, score, message, time):
        self.username = username
        self.score = score
        self.message = message
        self.time = time

    def __repr__(self):
        return '<User %r>' % self.username

    def as_dict(self):
        return {
                'username': self.username,
                'score': self.score,
                'message': self.message,
                'time': self.time,
                }


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

    # print(flask.request.get_json())
    json = flask.request.get_json()

    if ('username' not in json) or ('score' not in json) or ('message' not in json):
        flask.abort(400)

    now = datetime.datetime.now()
    message = Message(username=json['username'],
                      score=json['score'],
                      message=json['message'],
                      time=str(now.strftime("%Y-%m-%d %H:%M"))
                      )

    # # db vetos
    messages = Message.query.all()
    scores = [m.score for m in messages]
    usernames = [m.username for m in messages]
    highScoreTuple = list(zip(scores, usernames))
    # veto missing username
    if not message.username:
        return ''
    # veto same entry twice
    if (message.score, message.username) in highScoreTuple:
        print('Score', message.score, 'and username', message.username, 'alread present. Abort db submission!')
        return ''
    # veto entry of lower results
    userScores = [highScore[0] for highScore in highScoreTuple if highScore[1] == message.username]
    if userScores:
        highScore = max(userScores)
    else:
        highScore = 0
    if message.score < highScore:
        print('Score', str(message.score), ' less than existing highscore', str(highScore) + '. Abort db submission!')
        return ''

    db.session.add(message)
    db.session.commit()

    return ''
