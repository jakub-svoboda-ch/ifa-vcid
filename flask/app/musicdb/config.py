# musicdb/config.py
# Author: Jakub Svoboda <jakub.svoboda@gmx.ch>
# Copyright: CC0 or Beerware or WTFPL

# extensions imports
import redis

class data(object):
  FRONTEND_URL = "http://localhost:8080"
  SECRET_KEY = b'\x17\xcb\t\xb0\xe9\x17l\x12r\xa2\xd4\xf0\xb2\x12\xdaY'
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://musicdb:geheim@mysql/musicdb'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False
  SESSION_TYPE = 'redis'
  SESSION_PERMANENT = True
  SESSION_USE_SIGNER = True
  SESSION_REDIS = redis.from_url('redis://redis:6379')
  SESSION_COOKIE_SAMESITE = 'Lax'
  USE_SESSION_FOR_NEXT = True
  BOOTSTRAP_BOOTSWATCH_THEME = 'slate'
  SMTP_SERVER = "asmtp.yourhost.tld"
  SMTP_PORT = 587
  SMTP_USERNAME = "yourusername"
  SMTP_PASSWORD = "yourpassword"
  EMAIL_FROM = "musicdb@yourhost.tld"
