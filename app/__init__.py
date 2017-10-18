from __future__ import print_function

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


MAX_LENGTH_USERNAME = 20


class ScoreData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    score = db.Column(db.Integer)
    message = db.Column(db.String(80))
    time = db.Column(db.String(80))
    ip = db.Column(db.String(80))

    def __init__(self, username, score, message, time, ip):
        self.username = username[:MAX_LENGTH_USERNAME]
        self.score = score
        self.message = message
        self.time = time
        self.ip = ip

    def __repr__(self):
        return '<User %r>' % self.username

    def as_dict(self):
        return {
                'id': self.id,
                'username': self.username,
                'score': self.score,
                'message': self.message,
                'time': self.time,
                'ip': self.ip,
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
    scores = [e.as_dict() for e in entries]
    scores.sort(key=lambda x: x['score'], reverse=True)
    hsContent = ['username', 'score', 'time']
    dropLowerSame = 'username'
    allUserNames = set([score[dropLowerSame] for score in scores])
    idx = 1
    highScores = []
    for score in scores:
        if score[dropLowerSame] not in allUserNames:
            continue
        else:
            allUserNames.discard(score[dropLowerSame])
        for cont in score.keys():
            if cont not in hsContent:
                score.pop(cont, None)
        score['rank'] = idx
        highScores.append(score)
        idx += 1
    return flask.jsonify(highScores)


# ==============================================================================
# scores api
# ==============================================================================
@app.route('/scores', methods=['GET'])
def get_scores():
    entries = ScoreData.query.all()
    scores = [e.as_dict() for e in entries]
    scores.reverse()
    return flask.jsonify(scores)


@app.route('/scores', methods=['POST'])
def post_scores():
    if not flask.request.is_json:
        flask.abort(400)

    json = flask.request.get_json()

    if ('username' not in json) or ('score' not in json) or ('message' not in json):
        flask.abort(400)

    now = datetime.datetime.now()
    entry = ScoreData(username=json['username'],
                      score=json['score'],
                      message=json['message'],
                      time=now.strftime("%Y-%m-%d %H:%M:%S"),
                      ip=flask.request.remote_addr,
                      )

    # # db vetos
    entries = ScoreData.query.all()
    # veto missing username
    if not entry.username:
        return ''
    # veto same entry twice
    for thisEntry in entries:
        if entry.score == thisEntry.score and entry.username == thisEntry.username:
            print('Score', entry.score, 'and username', entry.username, 'alread present. Abort db submission!')
            return ''
    # veto entry of lower results
    userScores = [e.score for e in entries if e.username == entry.username]
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
