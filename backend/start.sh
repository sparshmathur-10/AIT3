#!/bin/bash
cd /opt/render/project/src/backend
gunicorn aitodo.wsgi:application --bind 0.0.0.0:$PORT 