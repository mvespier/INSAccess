"""
Module Name: models.py

Description:
    The models for the mariadb database

Author:
    Raphael Senellart

Date Created:
    January 22, 2025

Version:
    1.0.0

License:
    No License

Usage:
    should be called by init_db

Dependencies:


Notes:
    This tool is specialized for the agenda.insa-rouen.fr
    website, but some methods are generic and can be implemented
    else where.

"""

from flask_login import UserMixin
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy import Date, Time

from . import db


class User(UserMixin, db.Model):
    """User definition, inherit from UserMixin for authentication"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
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
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)

    date = db.Column(Date, nullable = False)
    start_hour = db.Column(Time)
    end_hour = db.Column(Time)
    desc = db.Column(db.String(255))
    

    link_td = db.relationship("ClassLinkTD", back_populates = "insa_class")
    link_teacher = db.relationship("ClassLinkTeacher", back_populates = "insa_class")
    link_room = db.relationship("ClassLinkRoom", back_populates = "insa_class")
    link_depart = db.relationship("ClassLinkDepart", back_populates = "insa_class")


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
    """ Room definition"""
    __tablename__ = 'room'
    name = db.Column(db.String(100), primary_key = True)





class ClassLinkTD(db.Model):
    """ 1 to Many link between classINSA and TD tables"""
    __tablename__ = 'class_link_td'

    class_id = db.Column(db.Integer, ForeignKey('insa_class.id'), primary_key = True)
    insa_class = db.relationship("InsaClass", back_populates="link_td")

    td_id = db.Column(ForeignKey('td_group.name'), primary_key = True)
    td = db.relationship("GroupTD")

class ClassLinkRoom(db.Model):
    """ 1 to Many link between classINSA and Room tables"""
    __tablename__ = 'class_link_room'

    class_id = db.Column(db.Integer, ForeignKey('insa_class.id'), primary_key = True)
    insa_class = db.relationship("InsaClass", back_populates="link_room")

    room_id = db.Column(ForeignKey('room.name'), primary_key = True)
    room = db.relationship("Room")

class ClassLinkTeacher(db.Model):
    """ 1 to Many link between classINSA and Teacher tables"""
    __tablename__ = 'class_link_teacher'

    class_id = db.Column(db.Integer, ForeignKey('insa_class.id'), primary_key = True)
    insa_class = db.relationship("InsaClass", back_populates="link_teacher")

    teacher_id = db.Column(ForeignKey('teacher.name'), primary_key = True)
    teacher = db.relationship("Teacher")

class ClassLinkDepart(db.Model):
    """ 1 to Many link between classINSA and Department tables"""
    __tablename__ = 'class_link_depart'

    class_id = db.Column(db.Integer, ForeignKey('insa_class.id'), primary_key = True)
    insa_class = db.relationship("InsaClass", back_populates="link_depart")

    depart_id = db.Column(ForeignKey('department.name'), primary_key = True)
    depart = db.relationship("Department")
