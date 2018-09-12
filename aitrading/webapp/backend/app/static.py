# coding=utf-8

from . import app

@app.route('/')
def root():
    return app.send_static_file('index.html')

