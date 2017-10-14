import datetime
import os

import flask
import flask_sqlalchemy

app = flask.Flask('foxApp')

# ==============================================================================
# configure frontend for interaction
# ==============================================================================
# select the database backend and where to find it
# os.environ['DATABASE_URL'] = 'http://127.0.0.1:5000/'  # uncomment to run with flask
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# suppress warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create db connection
db = flask_sqlalchemy.SQLAlchemy(app)


class ScoreData(db.Model):
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
# highscore api
# ==============================================================================
@app.route('/highscore', methods=['GET'])
def get_highscore():
    entries = ScoreData.query.all()
    return flask.jsonify([m.as_dict() for m in entries])


# ==============================================================================
# scores api
# ==============================================================================
@app.route('/scores', methods=['GET'])
def get_scores():
    entries = ScoreData.query.all()
    return flask.jsonify([m.as_dict() for m in entries])


@app.route('/scores', methods=['POST'])
def post_scores():
    if not flask.request.is_json:
        flask.abort(400)

    # print(flask.request.get_json())
    json = flask.request.get_json()

    if ('username' not in json) or ('score' not in json) or ('message' not in json):
        flask.abort(400)

    now = datetime.datetime.now()
    entry = ScoreData(username=json['username'],
                      score=json['score'],
                      message=json['message'],
                      time=now.strftime("%Y-%m-%d %H:%M:%S")
                      )

    # # db vetos
    entries = ScoreData.query.all()
    scores = [m.score for m in entries]
    usernames = [m.username for m in entries]
    highScoreTuple = list(zip(scores, usernames))
    # veto missing username
    if not entry.username:
        return ''
    # veto same entry twice
    if (entry.score, entry.username) in highScoreTuple:
        print('Score', entry.score, 'and username', entry.username, 'alread present. Abort db submission!')
        return ''
    # veto entry of lower results
    userScores = [highScore[0] for highScore in highScoreTuple if highScore[1] == entry.username]
    if userScores:
        highScore = max(userScores)
    else:
        highScore = 0
    if entry.score < highScore:
        print('Score', str(entry.score), ' less than existing highscore', str(highScore) + '. Abort db submission!')
        return ''

    db.session.add(entry)
    db.session.commit()

    return ''
