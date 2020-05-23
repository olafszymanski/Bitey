from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Optional, Length, DataRequired, Email, EqualTo, ValidationError
from .models import User


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[Optional(), Length(max=30)])
    last_name = StringField('Last name', validators=[Optional(), Length(max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)])
    repeat_password = PasswordField('Repeat password', validators=[EqualTo('password')])
    submit = SubmitField('Sign up')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already taken! Please try a different one.')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail is already taken! Please try a different one.')


class LogInForm(FlaskForm):
    username_or_email = StringField('Username or e-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')
