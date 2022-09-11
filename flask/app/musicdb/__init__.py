# musicdb/__init__.py
# Author: Jakub Svoboda <jakub.svoboda@gmx.ch>
# Copyright: CC0 or Beerware or WTFPL

# extensions imports
# for serverside sessions shared between mutliple flask containers
import redis
# import flask stuff
# https://flask.palletsprojects.com/en/2.1.x/
from flask import Flask, request, session
# flask serverside session support, connects to redis
# https://flask-session.readthedocs.io/en/latest/
from flask_session import Session
# manage user logins
# https://flask-login.readthedocs.io/en/latest/
from flask_login import LoginManager
# integrate SQLAlchemy into Flask
from flask_sqlalchemy import SQLAlchemy
# https://flask-wtf.readthedocs.io/en/1.0.x/csrf/
# https://wtforms.readthedocs.io/en/3.0.x/
from flask_wtf.csrf import CSRFProtect
# for nice looking html
# https://bootstrap-flask.readthedocs.io/en/stable/
from flask_bootstrap import Bootstrap5

# import our own application config
from . import config as cnf

# to get own IP in get_ip() & hostname
import socket

# get the IP of this flask container so we can
# display clearly which container served this request
def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.settimeout(0)
  try:
    # any IP will do, does not need to be reachable
    s.connect(('10.254.254.254', 1))
    IP = s.getsockname()[0]
  except Exception:
    IP = '127.0.0.1'
  finally:
    s.close()
  return IP

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config.from_object(cnf.data)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.globals['get_ip'] = get_ip
app.jinja_env.globals['gethostname'] = socket.gethostname

db = SQLAlchemy(app)

loginmanager = LoginManager(app)
loginmanager.login_view = 'user_login'
loginmanager.login_message = 'Sie müssen angemeldet sein für diese Aktion.'
loginmanager.login_message_category = "error"

Session(app)

csrf = CSRFProtect(app)

# import our core functionality
from . import routes, models, forms
