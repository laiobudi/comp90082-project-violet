# -*- coding:UTF-8 -*-

from flask import Flask, render_template, request, flash, redirect, url_for, make_response, Response, jsonify

import os, time

# sql
from flask_sqlalchemy import SQLAlchemy

def get32():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["SECRET_KEY"] = '123456'

# database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql://root:pwd@127.0.0.1/xxxtable'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

# db = SQLAlchemy()
# db.app = app
# db.init_app(app)


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':

    app.run(debug=True, threaded=True, port=5001, host='127.0.0.1')


