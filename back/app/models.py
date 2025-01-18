from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db
import enum
import sqlalchemy as sa
from sqlalchemy import ForeignKey


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
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    
    date = db.Column(db.String(10))
    start_hour = db.Column(db.String(8))
    end_hour = db.Column(db.String(8))
    desc = db.Column(db.String(255))

    
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
    user_id = db.Column(ForeignKey("user.id"))

class Student(db.Model):
    """ Student definition"""
    __tablename__ = 'student'
    user_id = db.Column(ForeignKey("user.id"), primary_key = True)
    department = db.Column(ForeignKey("department.name"))
    

class Room(db.Model):
    __tablename__ = 'room'
    name = db.Column(db.String(100), primary_key = True)


""" LINK TABLES """
class TDXClass(db.Model):
    __tablename__ = 'td_x_class'
    td_id = db.Column(ForeignKey('td_group.name'), primary_key = True)
    class_id = db.Column(ForeignKey('insa_class.id'), primary_key = True)

class RoomXClass(db.Model):
    __tablename__ = 'room_x_class'
    room_id = db.Column(ForeignKey('room.name'), primary_key = True)
    class_id = db.Column(ForeignKey('insa_class.id'), primary_key = True)

class TeacherXClass(db.Model): 
    __tablename__ = 'teacher_x_class'
    teacher_id = db.Column(ForeignKey('teacher.name'), primary_key = True)
    class_id = db.Column(ForeignKey('insa_class.id'), primary_key = True)

class DepartXClass(db.Model):
    __tablename__ = 'depart_x_class'
    depart_id = db.Column(ForeignKey('department.name'), primary_key = True)
    class_id = db.Column(ForeignKey('insa_class.id'), primary_key = True)

