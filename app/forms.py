from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    searchfield = StringField('Search field', validators=[DataRequired()])
    searchbutton = SubmitField('Search')