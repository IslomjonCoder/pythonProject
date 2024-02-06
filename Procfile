web: daphne -b 0.0.0.0 -p $PORT --ping-interval=0 config.asgi:application --settings=config.settings
worker: python manage.py runworker channels --settings=config.settings