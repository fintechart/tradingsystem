#!/bin/bash

export SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:myr00t@localhost:3306/tradingsystem'
export SECRET_KEY='nooneknows'

export FLASK_APP=./app/main.py
flask run -h 0.0.0.0
