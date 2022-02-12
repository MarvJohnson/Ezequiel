
web: gunicorn ezequiel_django.asgi:application -k uvicorn.workers.UvicornWorker
worker: daphne -p 8001 ezequiel_django.asgi:application
