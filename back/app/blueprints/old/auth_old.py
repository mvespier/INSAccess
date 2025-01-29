
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
