from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
import enum
import sqlalchemy as sa
from sqlalchemy import ForeignKey,ForeignKeyConstraint


class User(UserMixin, db.Model):
    """User definition, inherit from UserMixin for authentication"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # user information
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)
    name = db.Column(db.String(100))
    # admin field
    admin = db.Column(db.Boolean, default=False)
    # incremental user id - used for authentication
    seqid = db.Column(db.Integer, default=0)

    
class InsaClass(db.Model):
    """INSA Class definition,to store class from insa""" 
    __tablename__ = 'insa_class'
    date = db.Column(db.String(10))
    start_hour = db.Column(db.String(8), primary_key = True)
    end_hour = db.Column(db.String(8), primary_key = True)
    desc = db.Column(db.String(255), primary_key = True)

    
class GroupTD(db.Model):
    """ GroupTD definition """
    __tablename__ = 'td_group'
    name = db.Column(db.String(100), primary_key = True)

class Department(db.Model):
    """ Department definition """
    __tablename__ = 'department'
    name = db.Column(db.String(100), primary_key = True)


class Teacher(db.Model):
    """ Teacher definition"""
    __tablename__ = 'teacher'
    name = db.Column(db.String(255), primary_key = True)

class Student(db.Model):
    """ Student definition"""
    __tablename__ = 'student'
    user_id = db.Column(ForeignKey("user.id"), primary_key = True)
    department = db.Column(ForeignKey("department.name"))
    

class Room(db.Model):
    __tablename__ = 'room'
    name = db.Column(db.String(100), primary_key = True)


""" LINK TABLES """
class ClassLink(db.Model):
    __tablename__ = 'class_link'

    class_start_hour = db.Column(ForeignKey('insa_class.start_hour'), primary_key = True)
    class_end_hour = db.Column(ForeignKey('insa_class.end_hour'), primary_key = True)
    class_desc = db.Column(ForeignKey('insa_class.desc'), primary_key = True)
    insa_class = db.relationship("InsaClass")

    td_id = db.Column(ForeignKey('td_group.name'), nullable = False)
    td = db.relationship("GroupTD")
    room_id = db.Column(ForeignKey('room.name'), nullable = False)
    room = db.relationship("Room")
    teacher_id = db.Column(ForeignKey('teacher.name'), nullable = False)
    teacher = db.relationship("Teacher")
    depart_id = db.Column(ForeignKey('department.name'), nullable = False)
    depart = db.relationship("Department")



    __table_args__ = (
        ForeignKeyConstraint(['class_start_hour', 'class_end_hour', 'class_desc'],
         ['insa_class.start_hour', 'insa_class.end_hour','insa_class.desc']),
    )
