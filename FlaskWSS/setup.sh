#!/bin/bash

## First copy app.py file to project dir.
## From project dir run:
pip install python3.8-venv
python3 -m venv venvtest
source ./venvtest/bin/activate

## From inside venv
pip install flask flask-sock
flask run --host=0.0.0.0