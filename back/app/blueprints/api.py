"""
Module Name: api.py

Description:
    The blueprint for all the 
    informations communication with the front

Author:
    Raphael Senellart

Date Created:
    January 27, 2025

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
from flask import current_app, Blueprint,\
                  redirect, url_for, request, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from ..utils.db_insertion import insert_list_record
from ..utils.fetch import fetch_entire_year
from ..models import InsaClass, User, UserLinkTD, ClassLinkTD,GroupTD, db
from sqlalchemy.orm import joinedload
from time import strftime,strptime
import datetime



api = Blueprint('api', __name__,url_prefix='/api/')

@api.route('get_day/<string:day>')
@login_required
def get_day(day):
    """Return the json for the day"""
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    classes_subquery = get_class_of_user()

    insa_classes = (
        db.session.query(InsaClass)
        .options(
            joinedload(InsaClass.link_td),
            joinedload(InsaClass.link_teacher),
            joinedload(InsaClass.link_room),
            joinedload(InsaClass.link_depart),
        )
        .filter(InsaClass.id.in_(classes_subquery.select()), InsaClass.date == day_date)
        .all()
    )

    return get_json_output(insa_classes)

@api.route('get_week/<string:day>')
@login_required
def get_week(day):
    """Return the json for the week"""
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    start_of_week = day_date - datetime.timedelta(days=day_date.weekday())  # Monday
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Sunday

    classes_subquery = get_class_of_user()

    insa_classes = (
        db.session.query(InsaClass)
        .options(
            joinedload(InsaClass.link_td),
            joinedload(InsaClass.link_teacher),
            joinedload(InsaClass.link_room),
            joinedload(InsaClass.link_depart),
        )
        .filter(
        InsaClass.id.in_(classes_subquery.select()),
        InsaClass.date.between(start_of_week, end_of_week)  # Filter for the entire week
    )
        .all()
    )

    return get_json_output(insa_classes)

@api.route('get_month/<string:day>')
@login_required
def get_month(day):
    """Return the json for the month"""
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    start_of_month = day_date.replace(day=1)  # First day of the month
    end_of_month = (start_of_month + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)  # Last day of the month


    classes_subquery = get_class_of_user()

    insa_classes = (
        db.session.query(InsaClass)
        .options(
            joinedload(InsaClass.link_td),
            joinedload(InsaClass.link_teacher),
            joinedload(InsaClass.link_room),
            joinedload(InsaClass.link_depart),
        )
        .filter(
        InsaClass.id.in_(classes_subquery.select()),
        InsaClass.date.between(start_of_month, end_of_month)  # Filter for the entire week
    )
        .all()
    )

    return get_json_output(insa_classes)


@api.route('get_year/<string:day>')
@login_required
def get_year(day):
    """Return the json for the year """
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    start_of_year = day_date.replace(month=1,day=1)  # First day of the year
    end_of_year = (start_of_year + datetime.timedelta(days=400)).replace(day=1,month=1) - datetime.timedelta(days=1)  # Last day of the year


    classes_subquery = get_class_of_user()

    insa_classes = (
        db.session.query(InsaClass)
        .options(
            joinedload(InsaClass.link_td),
            joinedload(InsaClass.link_teacher),
            joinedload(InsaClass.link_room),
            joinedload(InsaClass.link_depart),
        )
        .filter(
        InsaClass.id.in_(classes_subquery).select(),
        InsaClass.date.between(start_of_year, end_of_year)  # Filter for the entire week
    )
        .all()
    )

    return get_json_output(insa_classes)


@api.route('/fetch')
@login_required
def fetch():
    list_of_records = fetch_entire_year("2024", "ITI", "3")
    insert_list_record(db.session, list_of_records)
    return "yippee"





def get_class_of_user():
    """transform the user tags to a classes_subquery"""
    tags_subquery = db.session.query(UserLinkTD.name_td)\
                    .filter_by(user_id=current_user.id).subquery()

    return db.session.query(ClassLinkTD.class_id)\
                    .filter(ClassLinkTD.td_id.in_(tags_subquery)).subquery()

def get_json_output(insa_classes):
    """transform the insa_class object in insa_class into a json for the front"""
    return jsonify([
        {
            "date": insa_class.date.strftime("%Y-%m-%d"),
            "start": insa_class.start_hour.strftime('%H:%M:%S'),
            "end": insa_class.end_hour.strftime('%H:%M:%S'),
            "desc": insa_class.desc,
            "td": [td.td.name for td in insa_class.link_td],
            "teacher": [teacher.teacher.name for teacher in insa_class.link_teacher],
            "room": [room.room.name for room in insa_class.link_room],
        }
        for insa_class in insa_classes
    ])