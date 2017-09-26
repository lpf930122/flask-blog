from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from flask_pagedown.fields import PageDownField


class LgForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class CommentForm(FlaskForm):
    body = TextAreaField('What\'s is your mind?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReplyForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    commentPath = StringField('', validators=[DataRequired()])
    submit = SubmitField('Send')
