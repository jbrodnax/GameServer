#!/bin/bash

# If deps are not installed:
# pip install python3.8-venv
# 

ROOT_PATH='~/flask-game-server'
PROJ_PATH="$ROOT_PATH/project"
VENV_NAME="venv-server"
VENV_PATH="$ROOT_PATH/$VENV_NAME"

echo "Starting 'install...'"

if [ ! -d $PROJ_PATH ]
then
    mkdir -p $PROJ_PATH
    echo "Created project folder: $PROJ_PATH"
fi

if [ ! -d VENV_PATH ]
then
    cd $ROOT_PATH && python3 -m venv $VENV_NAME
    echo "Created virtual env: $VENV_PATH"
fi

echo "Copying source files..."
cp ./FlaskWSS/*.py $PROJ_PATH
cp ./FlaskWSS/setup.sh $ROOT_PATH

echo "Finished."
echo "If deps have not been installed in the env, run:\npip install flask flask-sock flask-sqlalchemy flask-login"