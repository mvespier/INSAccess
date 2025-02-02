import time
from flask import current_app, Blueprint, render_template, redirect, send_from_directory, url_for, request, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


from ..models import User
from flask_mail import Message
from .. import db, mail, serializer
from ..utils.fetch import get_calendar_data
from ..utils.token import generate_token
import smtplib

main = Blueprint('main', __name__)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)


@main.route('/')
@login_required
def default_page():
    return render_template('index.html')

@main.route('/redirect')
def redirect_test():
    return redirect(url_for('main.default_page'))

@main.route('/<test>/redirect')
def var_test(test):
    return 'TOTO'

@main.route('/testmail')
def mail():
    token = generate_token(current_user.email)
    #confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
    html = render_template("accounts/confirm_email.html", confirm_url="confirm_url")
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    
    render_template('calendar_example.html')



@main.route('/calendar')
def calendar():
    return render_template('calendar_example.html')

@main.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')