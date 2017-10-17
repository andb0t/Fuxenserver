from __future__ import print_function

import argparse
import tabulate

import app

try:
    input = raw_input
except NameError:
    pass


def dict_table(dicts):
    print('Got response from server')
    try:
        keys = sorted(dicts[0].keys())
    except IndexError:
        print('No entry present')
        return
    table = []
    for d in dicts:
        table.append([d[key] for key in keys])
    print(tabulate.tabulate(table, headers=keys, tablefmt='grid'))


def create_db():
    print('Create db if non-existing')
    app.db.create_all()


def delete_db():
    print('Are you sure you want to delete the current database? (y/[n])')
    answer = input()
    if answer != 'y':
        return
    print('Delete db')
    app.db.drop_all()


def reset_db():
    print('Reset db')
    delete_db()
    create_db()


def show_db():
    entries = app.ScoreData.query.all()
    entryDicts = map(lambda x: x.as_dict(), entries)
    dict_table(entryDicts)


def show_entry(ID):
    print('Showing entry with ID', ID)
    entry = app.ScoreData.query.get(ID)
    if not entry:
        print('No matching entry found! Abort.')
        return
    dict_table([entry.as_dict()])


def delete_entry(ID):
    print('Deleting entry with ID', ID)
    entry = app.ScoreData.query.get(ID)
    if not entry:
        print('No matching entry found! Abort.')
        return
    app.db.session.delete(entry)
    app.db.session.commit()


def test_entry():
    print('Populating with test data')
    entry = app.Message(username='Test Entry',
                        score='0',
                        message='This is an automatically created test message.',
                        time='Arbitrary time')
    app.db.session.add(entry)
    app.db.session.commit()


parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='*', choices=['create', 'delete', 'reset', 'test_entry', 'show'])
parser.add_argument('--ID', default=0, type=int, help='ID of entry to show')
parser.add_argument('--all', action='store_true', default=False, help='Target entire database')
args = parser.parse_args()

for command in args.command:
    if args.all:
        if command == 'create':
            create_db()
        if command == 'delete':
            delete_db()
        if command == 'reset':
            reset_db()
        if command == 'show':
            show_db()
    else:
        if command == 'show':
            show_entry(args.ID)
        if command == 'delete':
            delete_entry(args.ID)
    if command == 'test_entry':
        test_entry()
