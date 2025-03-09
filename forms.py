from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class IssueForm(FlaskForm):
    title = StringField('Issue Title', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Issue')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ResponseForm(FlaskForm):
    response = TextAreaField('Response', validators=[DataRequired()])
    submit = SubmitField('Submit Response')
