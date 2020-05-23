from bitey import mail
from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(user):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    return serializer.dumps(user.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False

    return email


def send_email(subject, to, content):
    message = Message(subject, [to], html=content)
    mail.send(message)
