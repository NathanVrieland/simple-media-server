#! /bin/bash

cd $(dirname "$0")

source ./venv/bin/activate

gunicorn WSGI:app --bind=0.0.0.0:8000