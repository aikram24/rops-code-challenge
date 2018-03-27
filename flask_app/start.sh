#!/bin/bash
cd /tmp/repo/flask_app/
sudo -H pip install flask > install.log
#export FLASK_APP=app.py
python app.py > run.log 2>&1
