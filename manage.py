from __future__ import print_function

import argparse

import app


def create():
    print('Create db if non-existing')
    app.db.create_all()


def delete():
    print('Delete db')
    app.db.drop_all()


def reset():
    print('Reset db')
    delete()
    create()


def test_entry():
    print('Populating with test data')
    entry = app.Message(username='Test Entry',
                        score='0',
                        message='This is an automatically created test message.',
                        time='Arbitrary time')
    app.db.session.add(entry)
    app.db.session.commit()


parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='*', choices=['create', 'delete', 'reset', 'test_entry'])
args = parser.parse_args()

for command in args.command:
    if command == 'create':
        create()
    if command == 'delete':
        delete()
    if command == 'reset':
        reset()
    if command == 'test_entry':
        test_entry()
