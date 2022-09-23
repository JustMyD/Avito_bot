#!/bin/bash
exec pipenv shell
exec gunicorn -c "/home/www/Bot_projects/Avito_bot/gunicorn_config.py" config.wsgi
