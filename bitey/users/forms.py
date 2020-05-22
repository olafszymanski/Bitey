from flask_security.forms import Form, StringField, PasswordField, SubmitField, Length, Required, Email, EqualTo


class SignUpForm(Form):
    name = StringField('Name', validators=[Length(max=30)])
    last_name = StringField('Last name', validators=[Length(max=30)])
    username = StringField('Username', validators=[Required(), Length(min=5, max=30)])
    email = StringField('E-mail', validators=[Required(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[Required(), Length(min=8, max=200)])
    repeat_password = PasswordField('Repeat password', validators=[EqualTo('password')])
    submit = SubmitField('Sign up')


class LogInForm(Form):
    username_or_email = StringField('Username or e-mail', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log in')
