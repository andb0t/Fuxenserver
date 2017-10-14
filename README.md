# Fuxenserver

This is a small webserver to handle a high score list connected with the game Fuxensnake.

## Installation
Install heroku.

Create a virtualenv and execute `pip install -r requirements.txt`

## Server side

### Local
Start the heroku app locally with
```shell
heroku local local
```

### Web
Environmental variables accessible to heroku web can be set in `.env`. Special commands can be defined in `Procfile`.
```shell
heroku [COMMAND]  # use commands from `Procfile`
heroku run [COMMAND]  # run any command on heroku server
heroku run python manage.py recreate  # example, recreating the database
```


## Client side

### Local
```shell
python client.py [args]
python client.py --help  # get some info in usage
heroku local [COMMAND]  # use commands from `Procfile`
```

### Web
Communicate with the webserver as client:
```shell
python client.py --addr https://fuxenserver.herokuapp.com/messages
```
