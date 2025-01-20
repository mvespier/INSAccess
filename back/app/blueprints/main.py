import time
from flask import current_app, Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from flask_mail import Message
from .. import db, mail, serializer
from ..utils.fetch import get_calendar_data

main = Blueprint('main', __name__)

@main.route('/')
def default_page():
    return render_template('auth.html')

@main.route('/redirect')
def redirect_test():
    return redirect(url_for('main.default_page'))

@main.route('/<test>/redirect')
def var_test(test):
    return 'TOTO'
