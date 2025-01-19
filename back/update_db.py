from app import db, create_app
from app.utils import fetch
from app.models import *
from sqlalchemy.exc import IntegrityError


def insert_list_record(session, list_of_records):
    for record in list_of_records:
        insert_record_in_db(session, record)


def insert_record_in_db(session, record):
    date, start_hour, end_hour, desc = record[:4]
    room_list, teacher_list, td_list, depart_list = record[4:]
    insert_class_in_db(session, date, start_hour, end_hour, desc)
    
    for name in teacher_list:
        insert_teacher_in_db(session, name)

    for name in room_list:
        insert_room_in_db(session, name)
    
    for name in depart_list:
        insert_depart_in_db(session, name)

    for name in td_list:
        insert_groupTD_in_db(session, name)


def insert_class_in_db(session, date, start_hour, end_hour, desc):
    exists = session.query(InsaClass).filter_by(
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
    insert_generic_in_db(session, exists, new_class)

def insert_room_in_db(session, name):
    exists = session.query(Room).filter_by(
        name=name,
    ).first()
    
    new_class = Room(
        name=name,
    )
    insert_generic_in_db(session, exists, new_class)

def insert_depart_in_db(session, name):
    exists = session.query(Department).filter_by(
        name=name,
    ).first()
    
    new_class = Department(
        name=name,
    )
    insert_generic_in_db(session, exists, new_class)

def insert_teacher_in_db(session, name):
    exists = session.query(Teacher).filter_by(
        name=name,
    ).first()
    
    new_class = Teacher(
        name=name,
    )
    insert_generic_in_db(session, exists, new_class)

def insert_groupTD_in_db(session, name):
    exists = session.query(GroupTD).filter_by(
        name=name,
    ).first()
    
    new_class = GroupTD(
        name=name,
    )
    insert_generic_in_db(session, exists, new_class)


def insert_generic_in_db(session, exists, new_class):
    if not exists:
        try:
            session.add(new_class)
            session.commit()
            print("Inserted successfully.")
        except IntegrityError:
            session.rollback()
            print("Failed to insert due to integrity constraints.")
    else:
        print("Record already exists. No insertion performed.")
