import argparse

from app import Message
from app import db


def create():
    print('Creating db')
    db.create_all()


def delete():
    print('Deleting db')
    db.drop_all()


def recreate():
    print('Recreate db')
    delete()
    create()


def init():
    print('Populating with test data')
    message = Message(username='testpeep', message='This is generated when db is created.')
    db.session.add(message)
    db.session.commit()


parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='*', choices=['create', 'delete', 'recreate', 'init'])
args = parser.parse_args()

for command in args.command:
    if command == 'create':
        create()
    if command == 'delete':
        delete()
    if command == 'recreate':
        recreate()
    if command == 'init':
        init()
