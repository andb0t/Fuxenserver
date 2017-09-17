import socket
from flask import Flask

app = Flask('foxApp')


@app.route("/")
def index():
    return 'Hello from FLASK, my hostname is: %s \n' % (socket.gethostname())

# http://localhost:5000/
