from __future__ import print_function

import argparse
import tabulate

import app

try:
    input = raw_input
except NameError:
    pass


def dict_table(dicts):
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
    entryDicts = list(map(lambda x: x.as_dict(), entries))
    dict_table(entryDicts)


def show_entry(ID):
    print('Showing entry with ID', ID)
    entry = app.ScoreData.query.get(ID)
    if not entry:
        print('No matching entry found! Abort.')
        return
    dict_table([entry.as_dict()])


def show_filtered(key, val):
    print('Show entries with ', key, ':', val)
    entries = app.ScoreData.query.filter_by(**{key: val})
    entryDicts = list(map(lambda x: x.as_dict(), entries))
    dict_table(entryDicts)


def delete_entry(ID):
    print('Deleting entry with ID', ID)
    entry = app.ScoreData.query.get(ID)
    if not entry:
        print('No matching entry found! Abort.')
        return
    app.db.session.delete(entry)
    app.db.session.commit()


def execute_sql(sql):
    print('Execute this SQL command: "{0}"'.format(sql))
    # result = app.db.engine.execute(sql)
    # result = app.db.get_engine().execute(sql)
    result = app.db.session.execute(sql)
    for row in result:
        print(row)


def modify_entry(ID, key, val):
    print('Modifying entry with ID', ID, key, 'to', val)
    entry = app.ScoreData.query.get(ID)
    if not entry:
        print('No matching entry found! Abort.')
        return
    setattr(entry, key, val)
    app.db.session.commit()


def fill_test():
    print('Populating with test data')
    entry = app.Message(username='Test Entry',
                        score='0',
                        message='This is an automatically created test message.',
                        time='Arbitrary time',
                        ip='0.0.0.0',
                        )
    app.db.session.add(entry)
    app.db.session.commit()


parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='*', choices=['create', 'delete', 'reset', 'fill_test', 'show', 'modify', 'raw'])
parser.add_argument('--all', action='store_true', default=False, help='Target entire database')
parser.add_argument('--ID', default=None, type=int, help='ID of entry to show')
parser.add_argument('--sql', default=None, help='The SQL command to be executes')
parser.add_argument('--change', nargs='*', help='Specify database key and value')
parser.add_argument('--filter', nargs='*', help='Specify database key and value')
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
    elif args.ID is not None:
        if command == 'show':
            show_entry(args.ID)
        if command == 'delete':
            delete_entry(args.ID)
        if command == 'modify' and args.change:
            key, val = None, None
            try:
                key = args.change[0]
                val = args.change[1]
            except IndexError:
                print('IndexError: change requires two parameters!')
            if key and val:
                modify_entry(args.ID, key, val)
    elif args.filter:
        key, val = None, None
        try:
            key = args.filter[0]
            val = args.filter[1]
        except IndexError:
            print('IndexError: filter requires two parameters!')
        if key and val:
            if command == 'show':
                show_filtered(key, val)
    elif args.sql:
        if command == 'raw':
            execute_sql(args.sql)
    elif command == 'fill_test':
        fill_test()
    else:
        print('Command faulty, check the help!')
