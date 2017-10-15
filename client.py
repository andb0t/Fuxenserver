from __future__ import print_function

import argparse
import requests
import tabulate


def read_entries(addr):
    response = requests.get(addr)
    scores = response.json()

    print('Got response from server')
    try:
        keys = sorted(scores[0].keys())
    except IndexError:
        print('No entry present')
        return
    table = []
    for s in scores:
        table.append([s[key] for key in keys])
    print(tabulate.tabulate(table, headers=keys, tablefmt='grid'))


def post_entry(addr, username, score, message):
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
parser.add_argument('task', choices=['read', 'post'], help='Type of server interaction')
parser.add_argument('--addr', default='http://localhost:5000/',
                    help='Host adress (use \'web\' or \'local\' for predefined addresses)')
parser.add_argument('--name', default='', help='Name of user')
parser.add_argument('--msg', default='', help='Optional message')
parser.add_argument('--score', default=0, type=int, help='Achieved score')
parser.add_argument('--route', default='scores', help='Use this URL route string')
args = parser.parse_args()

if args.addr == 'web':
    args.addr = 'https://fuxenserver.herokuapp.com/'
elif args.addr == 'local':
    args.addr = 'http://localhost:5000/'

url = args.addr + args.route
print('Contacting', url, '...')
if args.task == 'post':
    print('Before insertion:')
    read_entries(url)
    post_entry(url, args.name, args.score, args.msg)
    print('After insertion:')
    read_entries(url)
elif args.task == 'read':
    read_entries(url)
