# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:09:30 2020

@author: peter
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '3f939fb9d12a33e42f9b9f9774daf16d0797fdbbaf658afd6a7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
from flaskblog import poem_generator
