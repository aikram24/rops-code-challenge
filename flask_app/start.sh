#!/bin/bash
cd /tmp/repo/flask_app/
pip install flask > install.log
export FLASK_APP=app.py
flask run > run.log 2>&1
