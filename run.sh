#! /bin/bash

gunicorn WSGI:app --bind=0.0.0.0:8000