# musicdb/models.py
# Author: Jakub Svoboda <jakub.svoboda@gmx.ch>
# Copyright: CC0 or Beerware or WTFPL

"""
Database Models for usage with Flask-SQLAlchemy
this module defines the following classes:

- `db_users`, representing the 'users' db table
- `db_genres`, representing the 'users' db table
- `db_artists`, representing the 'artists' db table
- `db_albums`, representing the 'albums' db table
- `db_songs`, representing the 'songs' db table

Functions:

- `load_user()`: custom user_loader for loginmanager

How To Use
==========
(See the individual classes, methods, and attributes for details.)

1. read https://flask.palletsprojects.com/en/2.1.x/patterns/sqlalchemy/
2. read https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

"""

__docformat__ = 'restructuredtext'

# extensions imports
# UserMixin is needed to extend the `db_users` object for login uses
from flask_login import UserMixin
# *_hash functions are needed for password hashing and checking
from werkzeug.security import generate_password_hash, check_password_hash
# used in the DB for actual timestamps `datetime.utcnow`
from datetime import datetime

# own source imports
# relative imports for our own objects
from . import db, loginmanager

@loginmanager.user_loader
def load_user(id):
  """custom user_loader for loginmanager."""
  return db_users.query.get(int(id))

class db_users(UserMixin, db.Model):
  """
  Base DB Table for Users Management

  see ERM/ERD for details

  Attributes
  ----------
  id : int
    primary_key for unique user id
  username : str
    unique displayname for the user, NOT used for login
  email : str
    unique address, used for login
  email_confirmed_at : datetime
    needs to be set together with 'active' to enable login
  password : str
    hashed password of the user account
  active : bool
    needs to be set to True together with 'email_confirmed_at'
  last_seen : datetime
    updated on every user request

  Methods
  -------
  set_password(password)
    hashes a new password and updates it
  check_password(password)
    returns True if supplied password matches the user stored one
  """

  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64))
  email = db.Column(db.String(255), unique=True)
  email_confirmed_at = db.Column(db.DateTime, unique=True)
  password = db.Column(db.String(128))
  active = db.Column(db.Integer)
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)

  def set_password(self, password):
    """set a new password hash"""
    self.password = generate_password_hash(password)

  def check_password(self, password):
    """check if supplied password is correct."""
    return check_password_hash(self.password, password)

class db_genres(db.Model):
  """
  Base DB Table for Genres

  see ERM/ERD for details

  Attributes
  ----------
  id : int
    primary_key for unique genres id
  genre : str
    unique name for the genre
  albums : relation
    sqlalchemy relationship back_populates

  Methods
  -------
  to_dict()
    returns a dict of the object

  """

  __tablename__ = 'genres'
  id = db.Column(db.Integer, primary_key=True)
  genre = db.Column(db.String(50))
  albums = db.relationship('db_albums', back_populates='genres')

  def to_dict(self):
    """returns a dict of the object"""
    return {
      'id': self.id,
      'genre': self.genre
    }

class db_artists(db.Model):
  """
  Base DB Table for Artists

  see ERM/ERD for details

  Attributes
  ----------
  id : int
    primary_key for unique artists id
  artist : str
    unique name for the artist/band/group
  albums : relation
    sqlalchemy relationship back_populates

  Methods
  -------
  to_dict()
    returns a dict of the object

  """

  __tablename__ = 'artists'
  id = db.Column(db.Integer, primary_key=True)
  artist = db.Column(db.String(200))
  albums = db.relationship('db_albums', back_populates='artists')

  def to_dict(self):
    """returns a dict of the object"""
    return {
      'id': self.id,
      'artist': self.artist
    }

class db_albums(db.Model):
  """
  Base DB Table for Albums

  see ERM/ERD for details

  Attributes
  ----------
  id : int
    primary_key for unique albums id
  genres_id : int
    foreign key to genres table
  artists_id : int
    foreign key to artists table
  year : str
    release year of the album
  album : str
    title of the album
  tracks : relation
    sqlalchemy relationship back_populates
  genres : relation
    sqlalchemy relationship back_populates
  artists : relation
    sqlalchemy relationship back_populates

  Methods
  -------
  to_dict()
    returns a dict of the object

  """

  __tablename__ = 'albums'
  id = db.Column(db.Integer, primary_key=True)
  genres_id = db.Column(db.Integer,db.ForeignKey('genres.id'))
  artists_id = db.Column(db.Integer,db.ForeignKey('artists.id'))
  year = db.Column(db.String(4))
  album = db.Column(db.String(200))
  tracks = db.relationship('db_songs', back_populates='albums')
  genres = db.relationship('db_genres', back_populates='albums')
  artists = db.relationship('db_artists', back_populates='albums')

  def to_dict(self):
    """returns a dict of the object"""
    return {
      'id': self.id,
      'genres_id': self.genres_id,
      'artists_id': self.artists_id,
      'year': self.year,
      'album': self.album,
      'tracks': self.tracks,
      'genre': self.genres.genre,
      'artist': self.artists.artist
    }

class db_songs(db.Model):
  """
  Base DB Table for Albums

  see ERM/ERD for details

  Attributes
  ----------
  id : int
    primary_key for unique songs id
  albums_id : int
    foreign key to albums table
  disc : int
    for multidisc releases
  track : int
    track number of the song
  title : str
    title of the song
  length : time
    duration of the song in hh:mm:ss
  albums : relation
    sqlalchemy relationship back_populates

  Methods
  -------
  to_dict()
    returns a dict of the object

  """

  __tablename__ = 'songs'
  id = db.Column(db.Integer, primary_key=True)
  albums_id = db.Column(db.Integer,db.ForeignKey('albums.id'))
  disc = db.Column(db.Integer)
  track = db.Column(db.Integer)
  title = db.Column(db.String(200))
  length = db.Column(db.Time)
  albums = db.relationship('db_albums', back_populates='tracks')

  def to_dict(self):
    """returns a dict of the object"""
    return {
      'id': self.id,
      'albums_id': self.albums_id,
      'disc': self.disc,
      'track': self.track,
      'title': self.title,
      'length': self.length
    }
