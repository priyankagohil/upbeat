# songs/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class MusicForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    album = StringField('Album')
    singer = StringField('Singer',validators=[DataRequired()])
    upload = FileField('Select mp3 file', validators=[FileAllowed(['mp3']),FileRequired()])
    submit = SubmitField("Upload")

class SearchForm(FlaskForm):
  search = StringField('Search with Title, Singer or Album', [DataRequired()])
  submit = SubmitField('Search')
