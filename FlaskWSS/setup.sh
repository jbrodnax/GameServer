#!/bin/bash

## First copy app.py file to project dir.
## From project dir run:
# pip install python3.8-venv
# python3 -m venv venvtest

## From inside venv
echo "run:"
echo 'export FLASK_APP=project'
echo 'export FLASK_DEBUG=1'
echo 'flask run --host=0.0.0.0'