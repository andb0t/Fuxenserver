import argparse
import requests


def read_messages(addr):
    response = requests.get(addr)
    messages = response.json()

    print('TODO: implement check for json data')

    print('Got response from server')
    for m in messages:
        print(m)
    print()


def post_message(addr, username, message):
    response = requests.post(addr,
                             json={'message': message,
                                   'username': username
                                   }
                             )
    # if request fails or throws error
    response.raise_for_status()


parser = argparse.ArgumentParser()
parser.add_argument('--addr', default='http://localhost:5000/messages')
args = parser.parse_args()

read_messages(args.addr)
post_message(args.addr, 'andb0t', 'Hi, posting message!')
read_messages(args.addr)
