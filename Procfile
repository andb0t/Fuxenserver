web: waitress-serve --port=$PORT app:app
local: waitress-serve --port=5000 app:app
start-db: python manage.py create init
recreate-db: python manage.py recreate
