import argparse

import app


def create():
    print('Creating db')
    app.db.create_all()


def delete():
    print('Deleting db')
    app.db.drop_all()


def recreate():
    print('Recreate db')
    delete()
    create()


def init():
    print('Populating with test data')
    message = app.Message(username='testbeep', score='0', message='This is generated when db is created.')
    app.db.session.add(message)
    app.db.session.commit()


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
