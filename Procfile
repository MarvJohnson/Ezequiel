
web: pipenv shell && pipenv install && python manage.py migrate && gunicorn ezequiel_django.asgi:application -k uvicorn.workers.UvicornWorker && daphne ezequiel_django.asgi:application
