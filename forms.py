from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class RegistratioForm(FlaskForm):
    username = StringField('Username', 
                                        validators = [])
    email = StringField()

class HomeStats(FlaskForm):
    shots = IntegerField('')
    target = IntegerField('')
    fouls = IntegerField('')
    corners = IntegerField('')
    yellow = IntegerField('')
    red = IntegerField('')
    submit = SubmitField('submit')

class AwayStats(FlaskForm):
    shots = IntegerField('')
    target = IntegerField('')
    fouls = IntegerField('')
    corners = IntegerField('')
    yellow = IntegerField('')
    red = IntegerField('')
    submit = SubmitField('submit')