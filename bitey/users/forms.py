from bitey import bcrypt
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Optional, Length, DataRequired, Email, EqualTo, ValidationError
from .models import User


class SignUpForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Optional(), Length(min=2, max=100)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)])
    repeat_password = PasswordField('Repeat Password', validators=[EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already taken! Please try a different one.')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail is already taken! Please try a different one.')


class LogInForm(FlaskForm):
    username_or_email = StringField('Username or E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class EditUserForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Optional(), Length(max=100)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=100)])
    username = StringField('Username', validators=[Optional(), Length(min=5, max=30)])
    email = StringField('E-mail', validators=[Optional(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save')


    def validate_username(self, field):
        if current_user.username != field.data and User.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already taken! Please try a different one.')


    def validate_email(self, field):
        if current_user.email != field.data and User.query.filter_by(email=field.data).first():
            raise ValidationError('This e-mail is already taken! Please try a different one.')


    def validate_password(self, field):
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('The password is incorrect!')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)])
    repeat_password = PasswordField('Repeat Password', validators=[EqualTo('password')])
    submit = SubmitField('Confirm')
