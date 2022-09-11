# musicdb/forms.py
# Author: Jakub Svoboda <jakub.svoboda@gmx.ch>
# Copyright: CC0 or Beerware or WTFPL

# extensions imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FieldList, FormField, IntegerField
from wtforms.validators import ValidationError, InputRequired, Email, Length, NumberRange, Regexp

# own source imports
# relative imports for our own objects
from .models import db_users

class form_user_login(FlaskForm):
        email = StringField('E-Mail', validators=[InputRequired()])
        password = PasswordField('Passwort', validators=[InputRequired()])
        remember_me = BooleanField('Angemeldet bleiben')

class form_user_register(FlaskForm):
        username = StringField('Benutzername', validators=[InputRequired(), Length(min=5, max=64)])
        email = StringField('Email', validators=[InputRequired(), Email(), Length(max=255)])
        password = PasswordField('Neues Passwort', validators=[InputRequired(), Length(min=12)])
        submit = SubmitField('Registrieren')
        def validate_username(self, username):
                user = db_users.query.filter_by(username=username.data).first()
                if user is not None:
                        raise ValidationError('Bitte verwenden Sie einen anderen Benutzernamen.')
        def validate_email(self, email):
                user = db_users.query.filter_by(email=email.data).first()
                if user is not None:
                        raise ValidationError('Bitte verwenden Sie eine andere E-Mail Adresse.')

class form_user_reset(FlaskForm):
        email = StringField('E-Mail', validators=[InputRequired(), Email(), Length(max=255)])

class form_user_password(FlaskForm):
        password = PasswordField('Neues Passwort', validators=[InputRequired(), Length(min=12)])

class form_track(FlaskForm):
        id = IntegerField('ID', validators=[InputRequired()])
        cd = SelectField('CD', validators=[InputRequired(), NumberRange(min=0, max=99)], choices=[(n, n) for n in range(101)], coerce=int)
        nr = SelectField('Nr.', validators=[InputRequired(), NumberRange(min=0, max=99)], choices=[(n, n) for n in range(101)], coerce=int)
        title = StringField('Titel', validators=[InputRequired(), Length(min=1, max=200)])
        length = StringField('Länge', validators=[InputRequired(), Regexp("(2[0-3]{1}|[0-1]{1}[0-9]{1}):([0-5]{1}[0-9]{1}):([0-5]{1}[0-9]{1})")])

class form_album(FlaskForm):
        artist = StringField('Künstler', validators=[InputRequired(), Length(max=200)])
        album = StringField('Album', validators=[InputRequired(), Length(max=200)])
        year = SelectField('Jahr', validators=[InputRequired(), NumberRange(min=1900, max=2022)], choices=[(n, n) for n in range(1900,2023)], coerce=int)
        genre = StringField('Genre', validators=[InputRequired(), Length(max=50)])
        tracks = FieldList(FormField(form_track), min_entries=1)
