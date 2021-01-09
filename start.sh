#!/usr/bin/env bash

export FLASK_ENV=testing

# gunicorn -b 127.0.0.1:8000 -k gevent -w 8 --threads 4 --max-requests 2000 wsgi:app -D

gunicorn -c gun.py  services.wsgi:app
