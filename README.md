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
```

### Web
Environmental variables accessible to heroku can be set in `.env`. Special commands can be defined in `Procfile`.
```shell
heroku [COMMAND]  # use commands from `Procfile`
heroku run [COMMAND]  # run any command on heroku server
heroku run python manage.py recreate  # example, recreating the database
```


## Client side

### Local
```shell
python client.py --help  # get some info in usage
python client.py --name Michael --msg "This is my message to you" --score 1  # example of usage
```

### Web
Communicate with the webserver as client:
```shell
python client.py --addr https://fuxenserver.herokuapp.com/messages [args]
```


## Database
The database is stored as flask sqlalchemy database. It can be managed with `manage.py` called via heroku. Here are some examples:
```shell
heroku [local] reset-db
```
