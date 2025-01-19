from app import db, create_app
from app.utils import fetch
from app.models import *

def insert_class_record_in_db(record):
    date, start_hour, end_hour, desc = record[:4]
    room_list, teacher_list, td_list, depart_list = record[4:]
    insert_class_in_db(date, start_hour, end_hour, desc)
    
    for name in teacher_list:
        insert_teacher_in_db(name) 

    

def insert_teacher_in_db(name):
    exists = db.session.query(Teacher).filter_by(
        name=name,
    ).first()
    
    new_class = Teacher(
        name=name,
    )
    insert_generic_in_db(exists, new_class)

def insert_class_in_db(date, start_hour, end_hour, desc):
    exists = db.session.query(InsaClass).filter_by(
        date=date,
        start_hour=start_hour,
        end_hour=end_hour,
        desc=desc
    ).first()

    new_class = InsaClass(
        date=date,
        start_hour=start_hour,
        end_hour=end_hour,
        desc=desc
    )
    insert_generic_in_db(exists, new_class)

def insert_generic_in_db(exists, new_class):
    if not exists:
        try:
            db.session.add(new_class)
            session.commit()
            print("Inserted successfully.")
        except IntegrityError:
            db.session.rollback()
            print("Failed to insert due to integrity constraints.")
    else:
        print("Record already exists. No insertion performed.")

