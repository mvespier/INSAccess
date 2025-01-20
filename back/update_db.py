from app import db, create_app
from app.utils import fetch
from app.models import *
from sqlalchemy.exc import IntegrityError


def insert_list_record(session, list_of_records):
    """ 
    ###insert_list_record :
    Insert the list of records (in this case fetched from insa.agenda)
    following the pattern : \n
    [(date, start_hour, end_hour, description, room_list, teacher_list, tdgroup_list, department_list), (...), ...]

    It is done by checking the existence of the record in the database and inserting it if necessary

    :param session: The current app session where the given records will be inserted
    :param list_of_records: The list of record to be inserted

    """
    for record in list_of_records:
        insert_record_in_db(session, record)


def insert_record_in_db(session, record):
    """
    ###insert_record_in_db : 
    Insert a single record in the given session
    following the pattern : \n
    (date, start_hour, end_hour, description, room_list, teacher_list, tdgroup_list, department_list)

    It is done by checking the existence of the record in the database and inserting it if necessary
    :param session: The current app session where the given record will be inserted
    :param record: The record to be inserted

    """
    date, start_hour, end_hour, desc = record[:4]
    room_list, teacher_list, td_list, depart_list = record[4:]
    
    insa_class = insert_class_in_db(session, date, start_hour, end_hour, desc)

    # SHOULD PROBABLY ONLY BE DONE ONCE IN A WHILE, NOT AT EVERY FETCH
    for name in teacher_list:
        insert_teacher_in_db(session, name)

    for name in room_list:
        insert_room_in_db(session, name)
    
    for name in depart_list:
        insert_depart_in_db(session, name)

    for name in td_list:
        insert_groupTD_in_db(session, name)

    # Insert ClassLink records to link InsaClass with associated entities
    for name in teacher_list:
        insert_classlink_teacher_in_db(session, insa_class, name)
    
    for name in room_list:
        insert_classlink_room_in_db(session, insa_class, name)
    
    for name in depart_list:
        insert_classlink_depart_in_db(session, insa_class, name)

    for name in td_list:
        insert_classlink_td_in_db(session, insa_class, name)



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
    if insert_generic_in_db(session, exists, new_class):
        return new_class
    return 

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

def insert_classlink_depart_in_db(session, insa_class, name):

    linked_entity = session.query(Department).filter_by(name=name).first()
    if linked_entity:
        exists = session.query(ClassLinkDepart).filter_by(
            class_start_hour=insa_class.start_hour,
            class_end_hour=insa_class.end_hour,
            class_desc=insa_class.desc,
            depart_id=name 
        ).first()

        class_link = ClassLinkDepart(
            insa_class=insa_class,
            depart=linked_entity
        )
        
        insert_generic_in_db(session, exists, class_link)
    else :
        print(f"Couldnt create link because {name} if not found in Department")

def insert_classlink_td_in_db(session, insa_class, name):

    linked_entity = session.query(GroupTD).filter_by(name=name).first()
    if linked_entity:
        exists = session.query(ClassLinkTD).filter_by(
            class_start_hour=insa_class.start_hour,
            class_end_hour=insa_class.end_hour,
            class_desc=insa_class.desc,
            td_id=name  # Check the td_id field (GroupTD name)
        ).first()

        class_link = ClassLinkTD(
            insa_class=insa_class,
            td=linked_entity
        )
        
        insert_generic_in_db(session, exists, class_link)
    else :
        print(f"Couldnt create link because {name} if not found in GroupTD")

def insert_classlink_room_in_db(session, insa_class, name):

    linked_entity = session.query(Room).filter_by(name=name).first()
    if linked_entity:
        exists = session.query(ClassLinkRoom).filter_by(
            class_start_hour=insa_class.start_hour,
            class_end_hour=insa_class.end_hour,
            class_desc=insa_class.desc,
            room_id=name  
        ).first()

        class_link = ClassLinkRoom(
            insa_class=insa_class,
            room=linked_entity
        )
        
        insert_generic_in_db(session, exists, class_link)
    else :
        print(f"Couldnt create link because {name} if not found in Room")

def insert_classlink_teacher_in_db(session, insa_class, name):

    linked_entity = session.query(Teacher).filter_by(name=name).first()
    if linked_entity:
        exists = session.query(ClassLinkTeacher).filter_by(
            class_start_hour=insa_class.start_hour,
            class_end_hour=insa_class.end_hour,
            class_desc=insa_class.desc,
            teacher_id=name  
        ).first()

        class_link = ClassLinkTeacher(
            insa_class=insa_class,
            teacher=linked_entity
        )
        
        insert_generic_in_db(session, exists, class_link)
    else :
        print(f"Couldnt create link because {name} if not found in Teacher")


def insert_generic_in_db(session, exists, new_class):
    """
    ###insert_generic_in_db:
    Method use by the others inserting methods in update_db\n
    Tries to insert in the database and if it create an Integrity error 
    rollsback the database to the given instance

    :param session: The current app session where the given record will be inserted
    :param exists:  A boolean given (typically a session.query to know if a record already exist)
    :param new_class: The transformed_record created by the calling methods

    """
    if not exists:
        try:
            session.add(new_class)
            session.commit()
            print("Inserted successfully.")
        except IntegrityError:
            session.rollback()
            print("Failed to insert due to integrity constraints.")
            return False
    else:
        print("Record already exists. No insertion performed.")
    return True

