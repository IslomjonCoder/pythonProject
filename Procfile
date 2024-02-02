web: gunicorn config.wsgi --log-file - --log-level info
websocket: daphne -b :: -p 5000 config.asgi:application
worker: gunicorn config.wsgi --log-file - --log-level info

dev: python manage.py runserver 0.0.0.0:8000

daphne: daphne -b 0.0.0.0 -p 8000 config.asgi

redis: redis-server


