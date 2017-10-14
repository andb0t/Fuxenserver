import argparse
import requests


def read_entries(addr):
    response = requests.get(addr)
    scores = response.json()

    print('Got response from server')
    for s in scores:
        print(s)
    print()


def post_entry(addr, username, score, message):
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


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--addr', default='http://localhost:5000/scores', help='Host adress')
parser.add_argument('--name', default='', help='Name of user')
parser.add_argument('--msg', default='', help='Optional message')
parser.add_argument('--score', default=0, type=int, help='Achieved score')
args = parser.parse_args()

read_entries(args.addr)
post_entry(args.addr, args.name, args.score, args.msg)
read_entries(args.addr)
