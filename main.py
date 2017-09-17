import socket
from flask import Flask

app = Flask('foxApp')


@app.route("/")
def index():
    return 'Hello from FLASK, my hostname is: %s \n' % (socket.gethostname())


if __name__ == "__main__":
    app.run(host='0.0.0.0')

# http://localhost:5000/
