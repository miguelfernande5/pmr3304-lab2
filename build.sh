#!/usr/bin/env bash
# Script de build usado no Render (Build Command: ./build.sh)
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python popular_banco.py
