#!/bin/bash
set -eu

export FLASK_APP=server.py
#export FLASK_DEBUG=1

virtualenv --python=python3 venv
venv/bin/pip install eventlet flask flask_socketio
exec venv/bin/python server.py
