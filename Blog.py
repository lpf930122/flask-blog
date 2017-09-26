#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import create_app

from app import db
from flask_login import login_required

app = create_app('default')


@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

 
@app.before_first_request
def before_request():
    db.create_all()

if __name__ == '__main__':
    app.run()
