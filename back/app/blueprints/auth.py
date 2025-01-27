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
import time
from flask import current_app, Blueprint, render_template,\
                  redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError


from ..models import User
from .. import db, mail, serializer


auth = Blueprint('auth', __name__)

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

@auth.route('/forgot_password')
def forgot_password():
    """ route for the forgot password html"""
    logout_user()
    return render_template('forgot_password.html')

@auth.route('/forgot_password', methods=['POST'])
def forgot_password_post():
    """ route for the forgot password function"""
    #checking if email is valid
    try:
        valid = validate_email(request.form['email'])   
    except EmailNotValidError as err:
        flash(f'email is wrong, please try again (error : {err})')
        return redirect(url_for('auth.forgot_password'))
    if not valid :
        flash('email is wrong, please try again')
        return redirect(url_for('auth.forgot_password'))

    #request the element from the form
    email = request.form.get('email')

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    if not user:
        return jsonify([False, "Cet user n'a pas de compte"])

    # create a token to be given within the reset password link
    data = {"i":str(user.id), "s": user.seqid, "t": int(time.time()/3600)}
    token = serializer.dumps(data)

    #create and send the mail to the user
    msg = Message(
                'Mot de passe oublié', 
                sender ='toto',
                recipients = [email]
    )
    msg.body = '''Hello,

        Vous recevez cet email car quelqu'un a demandé une réinitalisation de votre password
        sur %s. Si c'est bien vous, pour réinitialiser votre mot de passe, 
        rendez-vous sur cette url: %s%s''' % (current_app.config["APP_URL"], current_app.config["APP_URL"], url_for('auth.init_password', token=token))
    mail.send(msg)

    return jsonify([True, "Vérifiez vos emails"])

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

    db.session.add(User(email=email,
                                    name=name,
                                    password=generate_password_hash(new_password)))
    db.session.commit()
    flash("Success!")
    return redirect(url_for('auth.login'))



"""////////////////////////////////////////////////////////////////////////"""

@auth.route('/change_password')
def change_password():
    """route for loading the change_pwd html"""
    return render_template('change_password.html')

@auth.route('/change_password', methods=['POST'])
def change_password_post():
    """route for sending email to change password"""
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify([False, "Cet user n'a pas de compte"])

    data = {"i":str(user.id), "s": user.seqid, "t": int(time.time()/3600)}
    token = serializer.dumps(data)

    msg = Message( 
                'Mot de passe oublié', 
                sender ='toto', 
                recipients = [email]
    ) 
    msg.body = '''Hello, 

Vous recevez cet email car quelqu'un a demandé une réinitalisation de votre password
sur %s. Si c'est bien vous, pour réinitialiser votre mot de passe, 
rendez-vous sur cette url: %s%s''' % (current_app.config["APP_URL"], current_app.config["APP_URL"], url_for('auth.init_password', token=token))
    mail.send(msg)

    return jsonify([True, "Vérifiez vos emails"])


@auth.route('/init_password/<string:token>', methods=['GET'])
def init_password(token):
    """ route for changing password"""
    logout_user()

    data = serializer.loads(token)
    user = User.query.filter_by(id=data["i"]).first()

    if user.seqid != data["s"] or int(time.time()/3600)-data["t"] >= 1:
        flash('Le lien pour changer le password n\'est plus valide')
        return redirect(url_for('auth.login'))

    user.seqid = user.seqid+1
    db.session.commit()

    return render_template('new_password.html', email=user.email,\
                            token=serializer.dumps({"i":str(user.id), "s": user.seqid}))


@auth.route('/init_password', methods=['POST'])
def post_new_password():
    """ route for changing new password"""
    logout_user()

    data = serializer.loads(request.form.get('token'))
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(id=data["i"]).first()

    if user.seqid != data["s"]:
        flash('Le lien pour changer le password n\'est plus valide')
        return redirect(url_for('auth.login'))

    user.seqid = user.seqid+1
    user.password = generate_password_hash(password)
    db.session.commit()

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    """ route for disconnecting the user"""
    logout_user()
    return redirect(url_for('auth.login'))

