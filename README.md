# Fuxenserver

This is a small webserver to handle a high score list connected with the game Fuxensnake.

## Installation
* Install heroku
* create a virtualenv and execute `pip install -r requirements.txt`

## Server side

### Local
Start the heroku app locally with
```shell
heroku local local
heroku local [COMMAND]  # general way to use commands from `Procfile`
heroku local:run python manage.py reset  # execute custom commands
```

### Web
Environmental variables accessible to heroku can be set in `.env`. Special commands can be defined in `Procfile`.
```shell
heroku run [COMMAND]  # run any command on heroku server
heroku run python manage.py reset  # execute custom commands
```


## Client side

### Local
```shell
python client.py --help  # get some info in usage
python client.py post --name Michael --msg "This is my message to you" --score 1  # example for posting
python client.py read  # example for reading
```

### Web
Communicate with the webserver as client:
```shell
python client.py [TASK] --addr https://fuxenserver.herokuapp.com/ [args]  # explicit address
python client.py [TASK] --addr web [args]  # predefined address
```


## Database
The database is stored as flask sqlalchemy database. It can be managed with `manage.py` called via heroku. Here are some examples:
```shell
heroku [local] reset-db  # to use predefined commands
heroku [local:]run python manage.py --show --all  # show database contents
heroku [local:]run python manage.py --show --ID 1  # show entry with ID 1
heroku [local:]run python manage.py --modify --ID 1 --change score 0  # modify entry with ID 1
heroku [local:]run python manage.py --delete --ID 1  # delete entry with ID 1
heroku [local:]run python manage.py --show --filter username Simon  # show entries with specific username
```
