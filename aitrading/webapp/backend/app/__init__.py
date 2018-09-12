# coding=utf-8

import os
from flask_cors import CORS
from flask import Flask

# creating the Flask application
app = Flask(__name__)
CORS(app)

app_settings = os.getenv('APP_SETTINGS', 'app.config.DevelopmentConfig')
app.config.from_object(app_settings)

