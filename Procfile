web: gunicorn config.wsgi
worker: daphne -b 0.0.0.0 -p 8001 config.asgi:application