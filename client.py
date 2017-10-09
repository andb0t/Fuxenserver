import argparse
import requests


def read_messages(addr):
    response = requests.get(addr)
    messages = response.json()

    print('Got response from server')
    for m in messages:
        print(m)
    print()


def post_message(addr, username, score, message):
    print('TODO: implement check for json data')

    response = requests.post(addr,
                             json={
                                   'username': username,
                                   'score': score,
                                   'message': message,
                                   }
                             )
    # if request fails or throws error
    response.raise_for_status()


parser = argparse.ArgumentParser()
parser.add_argument('--addr', default='http://localhost:5000/messages')
parser.add_argument('--name', default='andb0t')
parser.add_argument('--msg', default='')
parser.add_argument('--score', default=0, type=int)
args = parser.parse_args()

read_messages(args.addr)
post_message(args.addr, args.name, args.score, args.msg)
read_messages(args.addr)
