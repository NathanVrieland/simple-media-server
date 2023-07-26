#! /bin/bash

cd $(dirname "$0")

./venv/bin/gunicorn WSGI:app --bind=0.0.0.0:8000
