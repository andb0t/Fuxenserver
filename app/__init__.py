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


class DailyMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(240))
    time = db.Column(db.String(80))
    category = db.Column(db.String(80))
    version = db.Column(db.String(80))

    def __init__(self, message, time, category, version):
        self.message = message
        self.time = time
        self.category = category
        self.version = version

    def __repr__(self):
        return '<Message %r>' % self.message

    def as_dict(self):
        return {
                'id': self.id,
                'message': self.message,
                'time': self.time,
                'category': self.category,
                'version': self.version,
                }


# ==============================================================================
# dummy api
# ==============================================================================
@app.route("/")
def index():
    return 'Hello from FLASK, my hostname is secret'
    # return 'Hello from FLASK, my hostname is: %s \n' % (socket.gethostname())


# ==============================================================================
# daily message api
# ==============================================================================
@app.route('/messages', methods=['GET'])
def get_messages():
    entries = DailyMessage.query.all()
    dailies = [e.as_dict() for e in entries]
    dailies.reverse()
    return flask.jsonify(dailies)


@app.route('/daily', methods=['GET'])
def get_daily():
    entry = db.session.query(DailyMessage).\
            filter(DailyMessage.category == 'news').\
            order_by(DailyMessage.id.desc()).\
            first()
    daily = None
    if entry:
        daily = entry.as_dict()
    return flask.jsonify([daily])


# ==============================================================================
# highscore api
# ==============================================================================
@app.route('/highscore', methods=['GET'])
def get_highscore():
    entries = ScoreData.query.all()
    scores = [e.as_dict() for e in entries]
    scores.sort(key=lambda x: x['score'], reverse=True)
    onlyCont = ['username', 'score', 'time']
    idx = 1
    highScores = []
    for score in scores:
        dropEntries = []
        for cont in score.keys():
            if cont not in onlyCont:
                dropEntries.append(cont)
        for drop in dropEntries:
            score.pop(drop, None)
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
