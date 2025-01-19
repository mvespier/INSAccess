from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash

from update_db import insert_list_record
from app.utils.fetch import get_calendar_data


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

    error_code, list_of_records = get_calendar_data('2024', 'ITI', '3', '20250120', 'week')

    if error_code == 0:
        insert_list_record(db.session, list_of_records)
        print("success")
    else :
        print(f"error {error_code} when fetching data")

    
