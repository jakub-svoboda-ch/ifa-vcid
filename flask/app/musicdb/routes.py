# musicdb/routes.py
# Author: Jakub Svoboda <jakub.svoboda@gmx.ch>
# Copyright: CC0 or Beerware or WTFPL

# extensions imports
# for timestamps
from datetime import datetime
from time import time
# for email sending
import smtplib
from email.message import EmailMessage
# for regex matching
import re
# for token generator in reset password and activate account
from itsdangerous import URLSafeTimedSerializer
# flask stuff
from flask import render_template, session, request, redirect, flash, url_for, Response, abort
from flask_login import login_user, logout_user, current_user, login_required

# own source imports
# relative imports for our own objects
from . import app, db
from .forms import form_user_login, form_user_register, form_user_reset, form_user_password, form_album, form_track
from .models import db_users, db_artists, db_genres, db_albums, db_songs

# for safe tokens to confirm email and reset password
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
# salted hashes and passwords taste better
salt = 'dVPbdxIjSlHHgnBGwbR0CmgCRrjurBFHMsTJMRtzKTiKdvWP3WbXWGKs0aJupQu4IWMR[]BC0F2pSC'

def send_mail(mailto, subject, route, template ):
  EMAIL_TO = mailto
  EMAIL_SUBJECT = subject
  
  # sign the mailaddress and use it as a token
  token = ts.dumps(EMAIL_TO, salt=salt)
  confirm_url = app.config['FRONTEND_URL'] + url_for(route, token = token)
  EMAIL_MESSAGE = render_template(template, confirm_url = confirm_url)

  # compose a message with correct headers
  msg = EmailMessage()
  msg.set_content(EMAIL_MESSAGE)
  msg['subject'] = EMAIL_SUBJECT
  msg['to'] = EMAIL_TO
  msg['from'] = app.config['EMAIL_FROM']

  try:
    # login to smtp server and send it
    s = smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT'])
    s.starttls()
    s.login(app.config['SMTP_USERNAME'], app.config['SMTP_PASSWORD'])
    s.send_message(msg, app.config['EMAIL_FROM'], EMAIL_TO)
    s.quit()
  except:
    flash("Fataler Fehler beim Versenden des E-Mails.", error)
    abort(500)

def check_token():
  token = request.args.get('token')
  try:
    email = ts.loads(token, salt=salt, max_age=86400)
    return email
  except:
    flash('Das Token ist nicht gültig!', 'error')
    return redirect(url_for('user_reset'))

"""
Flask App internal stuff
"""
@app.before_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/500')
def provoke500():
  abort(500)

@app.route('/favicon.ico')
def favicon():
  return redirect(url_for('static', filename='icons/favicon.ico'))

@app.route('/')
def index():
  stats_base = db.session.execute('''SELECT
@songs_c := (SELECT COUNT(*) FROM songs) as songs_c,
@artists_c := (SELECT COUNT(*) FROM artists) as artists_c,
@genres_c := (SELECT COUNT(*) FROM genres) as genres_c,
@albums_c := (SELECT COUNT(*) FROM albums) as albums_c,
@avg_songs_per_album := FORMAT(@songs_c / @albums_c, 0) as avg_songs_album,
@avg_songs_per_genre := FORMAT(@songs_c / @genres_c, 0) as avg_songs_genre,
@avg_songs_per_artist := FORMAT(@songs_c / @artists_c, 0) as avg_songs_artist
''')

  # --- top5 count songs per artist ---
  stats_songs_per_artist = db.session.execute('''SELECT artist, c
FROM (SELECT artists_id, COUNT(*) as c FROM songs GROUP BY artists_id ORDER BY c DESC LIMIT 0,5) as tbl1
JOIN artists ON (artists.id = tbl1.artists_id) ORDER BY c DESC
''')

  # --- top5 count albums per artist ---
  stats_albums_per_artist = db.session.execute('''SELECT artist, c
FROM (SELECT artists_id, COUNT(*) as c FROM albums GROUP BY artists_id ORDER BY c DESC LIMIT 0,5) as tbl1
JOIN artists ON (artists.id = tbl1.artists_id) ORDER BY c DESC
''')

  return render_template('index.html', title='Willkommen bei MusicDB', stats_base=stats_base, stats_songs_per_artist=stats_songs_per_artist, stats_albums_per_artist=stats_albums_per_artist)


@app.route('/impressum')
#@login_required
def impressum():
  return render_template('impressum.html', title='Impressum')



"""
User Management Routes
"""
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))

  form = form_user_login()

  next_page = session.get('next',url_for('index'))

  if form.validate_on_submit():
    user = db_users.query.filter_by(email=form.email.data).first()
    
    if user is not None and user.check_password(form.password.data):
      if user.active != 1:
        send_mail(user.email, ">> MusicDB Konto bestätigen", 'user_confirm', 'user_account_confirm.msg')
        flash('Dieses Konto ist nicht aktiviert. Sie haben eine E-Mail erhalten mit einem entsprechenden Link.', 'error')
        return redirect(url_for('user_reset'))
      login_user(user, remember=form.remember_me.data)
      flash('Guten Tag!')
      if session.get('next') != None:
        session.pop('next')
      return redirect(next_page)
    flash('Benutzername oder Passwort ungültig!', 'error')
    return redirect(url_for('user_login'))
  elif request.method == 'POST':
    flash('Benutzername oder Passwort ungültig!', 'error')
    return redirect(url_for('user_login'))
  return render_template('user_login.html', title='Anmelden', form=form, view='login')

@app.route('/user/logout')
def user_logout():
  logout_user()
  flash('Sie haben sich erfolgreich abgemeldet!')
  return redirect(url_for('user_login'))

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))

  form = form_user_register()

  if form.validate_on_submit():
    user = db_users(email=form.email.data, username=form.username.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()

    send_mail(user.email, ">> MusicDB Konto bestätigen", 'user_confirm', 'user_account_confirm.msg')

    flash('Willkommen! Sie sind nun ein registrierter Benutzer.')
    flash('Sie haben eine E-Mail erhalten. Bitte bestätigen Sie Ihr Konto.', 'error')
    return redirect(url_for('index'))

  if form.errors:
    flash('Bei der Registrierung ist etwas Fehlgeschlagen! Versuchen Sie es erneut.', 'error')
    session['error_email'] = form.email.data
    session['error_username'] = form.username.data
    session['error_password'] = form.password.data
    return redirect(url_for('user_register'))

  if session.get('error_email') is not None:
    form.email.data = session.pop('error_email')
    form.username.data = session.pop('error_username')
    form.password.data = session.pop('error_password')
    form.validate()
  return render_template('user_login.html', title='Registrieren', form=form, view='register')

@app.route('/user/confirm')
def user_confirm():
  if current_user.is_authenticated:
    return redirect(url_for('index'))

  email = check_token()

  user = db_users.query.filter_by(email=email).first()
  user.email_confirmed_at = datetime.utcnow()
  user.active = 1
  db.session.commit()
  flash('Ihr neues Konto wurde aktiviert.')
  return redirect(url_for('user_login'))

@app.route('/user/reset', methods=['GET', 'POST'])
def user_reset():
  if current_user.is_authenticated:
    return redirect(url_for('index'))

  form = form_user_reset()

  if form.validate_on_submit():
    user = db_users.query.filter_by(email=form.email.data).first()
    if user is None:
      flash('Diese E-Mail Adresse ist unbekannt.', 'error')
      return redirect(url_for('user_reset'))
    else:
      send_mail(user.email, ">> MusicDB Passwort zurücksetzen", 'user_password', 'user_password_reset.msg')
      flash('Eine E-Mail mit weiteren Angaben wurde versendet.')
      return redirect(url_for('user_login'))
  elif request.method == 'POST':
    flash('Geben Sie eine gültige E-Mail an.', 'error')
    return redirect(url_for('user_reset'))
  return render_template('user_login.html', title='Passwort zurücksetzen', form=form, view='reset')

@app.route('/user/password', methods=['GET', 'POST'])
def user_password():
  if current_user.is_authenticated:
    return redirect(url_for('index'))

  email = check_token()
  form = form_user_password()

  if form.validate_on_submit():
    user = db_users.query.filter_by(email=email).first()
    user.set_password(form.password.data)
    db.session.commit()
    flash('Ihr neues Passwort wurde gesetzt.')
    return redirect(url_for('user_login'))
  elif request.method == 'POST':
    flash('Geben Sie ein neues Passwort mit mindestens 12 Zeichen an.', 'error')
    return redirect(url_for('user_password', token=token))
  return render_template('user_password.html', title='Passwort zurücksetzen', form=form, token=token)

@app.route('/user/profile', methods=['GET', 'POST'])
def user_profile():
  form = form_user_register()
  user = db_users.query.filter_by(id=current_user.id).first()
  form.username.data = user.username
  form.email.data = user.email
  
  return render_template('user_profile.html', title='Benutzerprofil', form=form)


"""
MusicDB Routes
"""

@app.route('/musicdb/genres')
@login_required
def musicdb_genres():
  genres = db.session.execute('''
SELECT g.id, g.genre
FROM albums a RIGHT JOIN genres g ON (a.genres_id = g.id)
WHERE a.album IS NULL
''')
  return render_template('musicdb_genres.html', title='Genres', genres=genres)

@app.route('/musicdb/genres/delete/<int:genreid>')
@login_required
def musicdb_genres_delete(genreid=0):
  db.session.execute('''DELETE FROM genres WHERE id = :i ''', {'i':genreid})
  db.session.commit()
  flash('Genre wurde gelöscht.')
  return redirect(url_for('musicdb_genres'))

@app.route('/musicdb/artists')
@login_required
def musicdb_artists():
  artists = db.session.execute('''
SELECT tbl1.* FROM albums right JOIN
(SELECT ar.id, ar.artist
FROM songs s
RIGHT JOIN artists ar ON (s.artists_id = ar.id)
WHERE s.title IS NULL) AS tbl1
ON (tbl1.id=albums.artists_id)
WHERE albums.album IS NULL
''')
  return render_template('musicdb_artists.html', title='Künstler', artists=artists)

@app.route('/musicdb/artists/delete/<int:artistid>')
@login_required
def musicdb_artists_delete(artistid=0):
  db.session.execute('''DELETE FROM artists WHERE id = :i ''', {'i':artistid})
  db.session.commit()
  flash('Künstler wurde gelöscht.')
  return redirect(url_for('musicdb_artists'))

@app.route('/musicdb')
@app.route('/musicdb/albums')
#@login_required
def musicdb_albums():
  return render_template('musicdb_albums.html', title='Musikbibliothek')

# 2 little helper functions for create and edit routes
# - get_genre_id(name)
# - get_artist_id(name)

# get genre_id, if needed, create the genre first
def get_genre_id(name):
  genre_id = db_genres.query.filter_by(genre=name).first()
  if genre_id is None:
    db.session.add( db_genres(genre=name) )
    db.session.commit()
    genre_id = db_genres.query.filter_by(genre=name).first()
  return genre_id.id

# get artist_id, if needed, create the artist first
def get_artist_id(name):
  artist_id = db_artists.query.filter_by(artist=name).first()
  if artist_id is None:
    db.session.add( db_artists(artist=name) )
    db.session.commit()
    artist_id = db_artists.query.filter_by(artist=name).first()
  return artist_id.id


@app.route('/musicdb/albums/create', methods=['GET', 'POST'])
#@login_required
def musicdb_albums_create(albumid=0):

  form = form_album()

  # fetch helpertables for editable selects
  genres = db.session.execute("SELECT id, genre FROM genres")
  artists = db.session.execute("SELECT id, artist FROM artists")

  if request.method == 'POST' and form.validate_on_submit():
    album = db_albums(
          genres_id   = get_genre_id(form.genre.data),
          artists_id  = get_artist_id(form.artist.data),
          year        = form.year.data,
          album       = form.album.data
      )

    db.session.add(album)
    db.session.flush()

    for track in form.tracks.data:
      # insert new songs
      db.session.add( db_songs(
          albums_id = album.id,
          disc      = track['cd'],
          track     = track['nr'],
          title     = track['title'],
          length    = track['length']
       ) )

    db.session.commit()

    flash('Neues Album wurde erfasst.')
    return redirect(url_for('musicdb_albums_edit', albumid=album.id))
  else:
    if form.errors:
      flash('Album NICHT gespeichert. Prüfen Sie die Eingaben.', 'error')
      flash('Alle Felder müssen ausgefüllt werden.', 'error')
      return redirect(url_for('musicdb_albums_create'))

  return render_template('musicdb_albums_form.html', title='Neues Album eintragen', artists=artists, genres=genres, form=form)


@app.route('/musicdb/albums/edit/<int:albumid>', methods=['GET', 'POST'])
#@login_required
def musicdb_albums_edit(albumid=0):
  if albumid == 0:
    flash('Ungültige Albumid.', 'error')
    return redirect(url_for('musicdb_albums'))

  album = db_albums.query.filter_by(id=albumid).first()
  if album is None:
    flash('Dieses Album existiert nicht.', 'error')
    return redirect(url_for('musicdb_albums'))

  form = form_album()

  # fetch helpertables for editable selects
  genres = db.session.execute("SELECT id, genre FROM genres")
  artists = db.session.execute("SELECT id, artist FROM artists")

  if request.method == 'POST' and form.validate_on_submit():
    album.genres_id   = get_genre_id(form.genre.data)
    album.artists_id  = get_artist_id(form.artist.data)
    album.year        = form.year.data
    album.album       = form.album.data

    a = [(int(n['id'])) for n in form.tracks.data]
    b = [(n.id) for n in db_songs.query.filter_by(albums_id=albumid).all()]

    # delete songs in DB that are no longer present in the form
    for n in list( set(b) - set(a) ):
      db_songs.query.filter_by(id=int(n)).delete()

    for track in form.tracks.data:
      # update existing songs
      if track['id'] != 0:
        db_songs.query.filter_by( id=track['id'] ).update( dict(
            disc    = track['cd'],
            track   = track['nr'],
            title   = track['title'],
            length  = track['length']
            ) )
      # insert new songs
      else:
        db.session.add( db_songs(
            albums_id = albumid,
            disc      = track['cd'],
            track     = track['nr'],
            title     = track['title'],
            length    = track['length']
          ) )

    db.session.commit()
    flash('Album wurde aktualisiert.')
    return redirect(url_for('musicdb_albums_edit', albumid=albumid))

  else:
    if form.errors:
      flash('Illegale Eingaben. Versuchen Sie es erneut.', 'error')
      flash('Alle Felder müssen ausgefüllt werden.', 'error')
      return redirect(url_for('musicdb_albums_edit', albumid=albumid))

  return render_template('musicdb_albums_form.html', title='Album bearbeiten', artists=artists, genres=genres, album=album, form=form)


@app.route('/musicdb/albums/delete/<int:albumid>')
#@login_required
def musicdb_albums_delete(albumid=0):
  if albumid != 0:
    db_songs.query.filter_by(albums_id=albumid).delete()
    db_albums.query.filter_by(id=albumid).delete()
    db.session.commit()

    flash('Album wurde gelöscht.')
    return redirect(url_for('musicdb_albums'))


@app.route('/musicdb/api')
#@login_required
def musicdb_api():
  return render_template('musicdb_api.html', title='MusicDB API')


"""
MusicDB API Routes
"""
# this route is used in the frontend.
# the other 2 routes where used to test the speed of SQL queries
@app.route('/api/albums')
#@login_required
def api_albums():

  # get filter params from url
  # search=query
  search = request.args.get('search')
  # sort=[+|-]attr,[+|-]attr
  sort = request.args.get('sort')

  # pagination
  start = request.args.get('start', type=int, default=0)
  length = request.args.get('length', type=int, default=10)

  sql_search = ''
  sql_orderby = ''
  sql_paginate = 'LIMIT ' + str(start) + ', ' + str(length)

  # create the WHERE clause for searching
  if search and search != '':
    if re.match("^[ A-Za-z0-9-]*$", search):
      sql_search = "WHERE artist LIKE '%" + search + "%' OR album LIKE '%" + search + "%' OR title LIKE '%" + search + "%' OR genre LIKE '%" + search + "%'"

  # process sort= query part and build ORDER BY ...
  if sort and sort != '':
    if re.match(r'([+-])(artist|year|album|genre|disc|track|title|length)[,]*', sort):
      orderby = []
      for s in sort.split(','):
        ascdesc = s[0]
        name = s[1:]
        # check if key is valid
        if name in ['artist', 'year', 'album', 'genre', 'disc', 'track', 'title', 'length']:
          if ascdesc == '-':
            orderby.append( name + ' DESC')
          if ascdesc == '+':
            orderby.append( name + ' ASC')
      if orderby:
        sql_orderby = 'ORDER BY ' + ', '.join(orderby)
  else:
    # we have no sort= so let's set a sane default
    sql_orderby = 'ORDER BY artist ASC, year ASC, album ASC, disc ASC, track ASC'

  sql_string = '''
SELECT so.albums_id, al.genres_id, al.artists_id, ar.artist, al.year, al.album, ge.genre, so.disc, so.track, so.title, so.length
FROM albums al
JOIN genres ge ON (ge.id = al.genres_id)
JOIN artists ar ON (ar.id = al.artists_id)
JOIN songs so ON (al.id = so.albums_id)
'''
  # hit the DB server one more time only to get max rows for paginating
  albums_totals = db.session.execute(sql_string + sql_search)

  sql_string = sql_string + sql_search + '''
''' + sql_orderby + '''
''' + sql_paginate

  # perform the real query with all sorting and paginating
  albums = db.session.execute(sql_string)

  # the jinja2 template assembles all rows to JSON object
  return Response(render_template('albums.json', albums=albums, total=albums_totals.rowcount), mimetype="application/vnd.api+json")




# raw SQL command with SQLAlchemy without ORM stuff
# JSON is generated mostly directyl in MySQL Server
# resulting recordset is already a collection of jsonified rows
# jinja2 template only joins the rows together
# 1141 Albums with a total of 15576 songs => 1.48MB => between 110ms and 200ms
# that seems very usable for a fast API
@app.route('/api/albums-raw')
#@login_required
def api_albums_raw():

  # GROUP_CONCAT default length is only 1024 bytes
  db.session.execute('''SET group_concat_max_len = 888888''')
  db.session.commit()

  # JOIN all tables, get JSON for GROUPed BY songs for each ALBUM
  # then CONCAT every row to one JSON object
  albums = db.session.execute('''
SELECT CONCAT('{ "album_id": ', al.id, ',\n',
    '"genres_id": ', al.genres_id, ',\n',
    '"artists_id": ', al.artists_id, ',\n',
    '"album": "', al.album, '",\n',
    '"year": ', al.year, ',\n',
    '"genre": "', ge.genre, '",\n',
    '"artist": "', ar.artist, '",\n',
    '"tracks": [', songlist.JSON, ']}') as tracks
FROM albums al
JOIN genres ge ON (ge.id = al.genres_id)
JOIN artists ar ON (ar.id = al.artists_id)
JOIN (
  SELECT aid, GROUP_CONCAT(jsontable.JSON separator ',') as JSON
  FROM (
    SELECT so.albums_id as aid, CONCAT('{"id": ', so.id, ',\n',
'"disc": ', so.disc, ',\n', '"track": ', so.track, ',\n', '"title": "', 
REPLACE(so.title, '"', ''), '",\n', '"length": "', so.length, '"}') as JSON FROM songs so ORDER BY so.disc, so.track ) AS jsontable GROUP BY aid) as songlist ON (al.id = songlist.aid)
ORDER BY ar.artist, al.year, al.album
;''')

  # the jinja2 template only assembles all JSON row objects in one big JSON object
  return Response(render_template('albums_raw.json', albums=albums, total=albums.rowcount), mimetype="application/json")


# very slow SQLAlchemy ORM Style of JOINing and sorting
# 1141 Albums with a total of 15576 songs => 1.48MB => 10 seconds
# not really usable for a fast API
@app.route('/api/albums-orm')
#@login_required
def api_albums_orm():

  # JOIN the artists table, to be able to sort on artists
  albums = db_albums.query.join(db_artists)
  # for each order by get the db-table attributes
  albums = albums.order_by(getattr(db_artists, 'artist'))
  albums = albums.order_by(getattr(db_albums, 'year'))
  albums = albums.order_by(getattr(db_albums, 'album'))

  # execute the query
  albumlist = albums.all()
  # the jinja2 template has to do the hard work of assembling a JSON object
  return Response(render_template('albums_orm.json', albums=albumlist, total=albums.count()), mimetype="application/json")


