#!/bin/bash
set -e
python -m gunicorn --bind 0.0.0.0:${PORT:-5000} wsgi:app
