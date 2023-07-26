#! /bin/bash

cd $(dirname "$0")

./venv/bin/gunicorn WSGI:app
