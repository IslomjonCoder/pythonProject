web: daphne -b 0.0.0.0 -p $PORT --ping-interval=0 config.asgi:application
worker: python manage.py runworker channels --settings=config.settings
redis: docker run -p 6379:6379 -d redis:5
