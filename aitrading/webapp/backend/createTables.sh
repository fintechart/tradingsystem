#!/bin/bash

export SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:myr00t@localhost:3306/tradingsystem'

python -m app.entities

