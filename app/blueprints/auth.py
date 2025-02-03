"""
Module Name: auth.py

Description:
    The blueprint for all the interaction 
    related to authentification

Author:
    Raphael Senellart

Date Created:
    January 18, 2025

Version:
    1.0.0

License:
    No License

Usage:
    should be initialized in the app factory
    and is used by the flask server

Dependencies:


Notes:
    This tool is specialized for the agenda.insa-rouen.fr
    website, but some methods are generic and can be implemented
    else where.

"""
from flask import current_app, Blueprint, render_template,\
                  redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required,\
                    current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError

from ..utils.token import confirm_token, generate_token, send_email

from ..utils.decorator import logout_required


from ..models import User
from .. import db, mail, serializer

auth = Blueprint('auth', __name__)
""""""


"""////////////////////////////////////////////////////////////////////////"""

@auth.route('/login')
def login():
    """route for login"""
    logout_user()
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """ route for login"""

    #request the elements from the form
    request_dict = request.form
    email = request_dict.get('email')
    password = request_dict.get('password')
    remember = True if request_dict.get('remember') else False

    #checking if email is valid
    try:
        valid = validate_email(email)
    except EmailNotValidError as err:
        flash(f'email is wrong, please try again (error : {err})')
        return redirect(url_for('auth.login'))
    if not valid :
        flash('email is wrong, please try again')
        return redirect(url_for('auth.login'))



    user = User.query.filter_by(email=email).first()
    # here the first() is used only to increase the speed, since email is unique

    # check if the user actually exists
    # take the user-supplied password, hash it,
    #  and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Mot de passe incorrect')
        return render_template('login.html', email = email)

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.default_page'))

"""////////////////////////////////////////////////////////////////////////"""

@auth.route('/sign_up')
def sign_up():
    """ route for loading the signing up html"""
    logout_user()
    return render_template('sign_up.html')


@auth.route('/sign_up', methods =['POST'])
def sign_up_post():
    """ route for signing up"""
    logout_user()
    #check if email is valid

    request_dict = request.form
    name = request_dict.get('name')
    email = request_dict.get('email')
    new_password = request_dict.get('new_password')
    confirmed_password = request_dict.get('confirmed_password')

    try:
        valid = validate_email(email)
    except EmailNotValidError as err:
        flash(f'email is wrong, please try again {err}')
        return redirect(url_for('auth.sign_up'))
    if not valid or not email.endswith('@insa-rouen.fr'):
        flash('email is wrong, please try again (use insa\'s email)')
        return redirect(url_for('auth.sign_up'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('cet email est deja utilisé')
        return render_template('sign_up.html', name=name, email=email)

    if new_password != confirmed_password:
        flash("les mdp ne sont pas egaux")
        return render_template('sign_up.html', name=name, email=email)

    token = generate_token({'email' : email,
                            'name' : name,
                            'password' : new_password
                            })
    confirm_url = url_for("auth.confirm_sign_up", token=token, _external=True)
    html = render_template("email_confirmation.html", confirm_url=confirm_url)
    subject = "Validation du compte INSAccess"
    send_email(email, subject, html)

    flash("Finalisez votre creation de compte en regardant votre boite mail!")
    return redirect(url_for('auth.login'))

@auth.route('/confirm_sign_up/<token>', methods =['GET'])
@logout_required
def confirm_sign_up(token):

    values = confirm_token(token)
    email = values.get('email')
    name = values.get('name')
    password = values.get('password')
    
    try:
        valid = validate_email(email)
    except EmailNotValidError as err:
        return redirect(url_for('auth.sign_up'))
    if not valid or not email.endswith('@insa-rouen.fr'):
        return redirect(url_for('auth.sign_up'))

    user = User.query.filter_by(email=email).first()

    if user:
        return redirect(url_for('auth.sign_up'))
    

    db.session.add(User(email=email,
                        name=name,
                        password=generate_password_hash(password)))
    db.session.commit()
    
    flash("Success!")
    return redirect(url_for('auth.login'))
    

"""////////////////////////////////////////////////////////////////////////"""

@auth.route('/logout')
@login_required
def logout():
    """ route for disconnecting the user"""
    logout_user()
    return redirect(url_for('auth.login'))

