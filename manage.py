from __future__ import print_function

import argparse
import datetime
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


def get_table(table):
    if table == 'scores':
        return app.ScoreData
    elif table == 'messages':
        return app.DailyMessage


def show_table(table):
    print('Table', table, 'content:')
    entries = get_table(table).query.all()
    entryDicts = list(map(lambda x: x.as_dict(), entries))
    dict_table(entryDicts)


def show_db():
    show_table('scores')
    show_table('messages')


def get_entry(ID, table):
    entry = get_table(table).query.get(ID)
    if not entry:
        print('No matching entry found! Abort.')
        return None
    return entry


def show_entry(ID, table):
    print('Showing entry in table', table, 'with ID', ID)
    entry = get_entry(ID, table)
    if not entry:
        return
    dict_table([entry.as_dict()])


def delete_entry(ID, table):
    print('Deleting entry in table', table, 'with ID', ID)
    entry = get_entry(ID, table)
    if not entry:
        return
    app.db.session.delete(entry)
    app.db.session.commit()


def modify_entry(ID, table, key, val):
    print('Modifying entry in table', table, 'with ID', ID, key, 'to', val)
    entry = get_entry(ID, table)
    if not entry:
        return
    setattr(entry, key, val)
    app.db.session.commit()


def show_filtered(table, key, val):
    print('Show entries with ', key, ':', val)
    entries = get_table(table).query.filter_by(**{key: val})
    entryDicts = list(map(lambda x: x.as_dict(), entries))
    dict_table(entryDicts)


def execute_sql(sql):
    print('Execute this SQL command: "{0}"'.format(sql))
    # result = app.db.engine.execute(sql)
    # result = app.db.get_engine().execute(sql)
    result = app.db.session.execute(sql)
    for row in result:
        print(row)


def fill_test():
    print('Populating with test data')
    now = datetime.datetime.now()
    entry = app.ScoreData(username='Test Entry',
                          score='0',
                          message='This is an automatically created test message.',
                          time=now.strftime("%Y-%m-%d %H:%M:%S"),
                          ip='0.0.0.0',
                          )
    app.db.session.add(entry)
    app.db.session.commit()


def post_news(message, category, version='all'):
    print('Submitting news message (' + version, ',', category+'):', message)
    now = datetime.datetime.now()
    entry = app.DailyMessage(message=message,
                             time=now.strftime("%Y-%m-%d %H:%M:%S"),
                             category=category,
                             version=version,
                             )
    app.db.session.add(entry)
    app.db.session.commit()


def drop_message_table(table):
    get_table(table).__table__.drop(app.db.engine)


parser = argparse.ArgumentParser()
parser.add_argument('command', nargs='*', choices=['create', 'delete', 'reset', 'fill_test',
                                                   'show', 'modify',
                                                   'raw',
                                                   'news', 'alert', 'version'])
parser.add_argument('--all', action='store_true', default=False, help='Target entire database')
parser.add_argument('--table', default='scores', choices=['scores', 'messages'], help='Target database table')
parser.add_argument('--ID', default=None, type=int, help='ID of entry to show')
parser.add_argument('--change', nargs='*', help='Specify database key and value')
parser.add_argument('--filter', nargs='*', help='Specify database key and value')
parser.add_argument('--sql', default=None, help='The SQL command to be executes')
parser.add_argument('--msg', default=None, help='Daily message')
parser.add_argument('--version', default='all', help='Daily message for all versions lower than this')
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
            show_entry(args.ID, args.table)
        if command == 'delete':
            delete_entry(args.ID, args.table)
        if command == 'modify' and args.change:
            key, val = None, None
            try:
                key = args.change[0]
                val = args.change[1]
            except IndexError:
                print('IndexError: change requires two parameters!')
            if key and val:
                modify_entry(args.ID, args.table, key, val)
    elif args.filter:
        key, val = None, None
        try:
            key = args.filter[0]
            val = args.filter[1]
        except IndexError:
            print('IndexError: filter requires two parameters!')
        if key and val:
            if command == 'show':
                show_filtered(args.table, key, val)
    elif args.table:
        show_table(args.table)
    elif args.msg:
        if command == 'news':
            post_news(args.msg, 'news')
        elif command == 'alert':
            post_news(args.msg, 'alert', args.version)
        elif command == 'version' and args.version != 'all':
            post_news(args.msg, 'release', args.version)
    elif args.sql:
        if command == 'raw':
            execute_sql(args.sql)
    elif command == 'fill_test':
        fill_test()
    else:
        print('Command faulty, check the help!')
