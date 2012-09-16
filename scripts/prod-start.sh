#!/bin/bash
#PORT=8080
#python worldofloot/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3 -k gevent --preload
worldofloot/manage.py supervisor --daemonize
echo 'Done.'
