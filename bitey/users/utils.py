from bitey import mail
from flask import current_app, copy_current_request_context, url_for, render_template
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from threading import Thread


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


def send_activation_email(user, title, body):
    @copy_current_request_context
    def send():
        token = generate_confirmation_token(user)
        url = url_for('users.activation', token=token, _external=True)
        content = render_template('users/emails/activation.html', username=user.username, body=body, url=url)
        send_email(title, user.email, content)

    sender = Thread(name='email_sender', target=send)
    sender.start()
