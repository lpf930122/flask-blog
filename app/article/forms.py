from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    hide = BooleanField('不公开')
    submit = SubmitField('Submit')