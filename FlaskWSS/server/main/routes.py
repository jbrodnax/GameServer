from flask import Blueprint
from .. import db
from . import main

@main.route('/')
def index():
    tmp = '{"hello":"world"}'
    return tmp
