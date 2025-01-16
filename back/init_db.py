from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash


with create_app().app_context():

    db.create_all()

    with open("data/users.txt") as f:
        for line in f:
            if not line.startswith("#") or line.startswith('\n'):
                (email, name) = line.strip().split("\t")
                db.session.add(User(email=email,
                                    name=name,
                                    password=generate_password_hash("password-rco",)))
                                    
    db.session.commit()
