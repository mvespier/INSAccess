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

import datetime

from sqlalchemy.orm import joinedload
from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_required

from ..utils.db_insertion import insert_list_record
from ..utils.fetch import fetch_entire_year
from ..models import EnumColor, EnumSector, EnumType, InsaClass, UserLinkTD, ClassLinkTD, db


api = Blueprint('api', __name__,url_prefix='/api/')

@api.route('get_day/<string:day>',methods =["GET"])
@login_required
def get_day(day):
    """Return the json for the day"""
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    classes_subquery = get_class_of_user()

    insa_classes = (
    get_joined_class_subquery().filter(
        InsaClass.id.in_(classes_subquery), InsaClass.date == day_date
        )
        .all()
    )

    return get_json_output(insa_classes)

@api.route('get_week/<string:day>',methods =["GET"])
@login_required
def get_week(day):
    """Return the json for the week"""
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    start_of_week = day_date - datetime.timedelta(days=day_date.weekday())  # Monday
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Sunday

    classes_subquery = get_class_of_user()

    insa_classes = (
        get_joined_class_subquery().filter(
            InsaClass.id.in_(classes_subquery),
            InsaClass.date.between(start_of_week, end_of_week)  # Filter for the entire week
        )
        .all()
    )

    return get_json_output(insa_classes)

@api.route('get_month/<string:day>',methods =["GET"])
@login_required
def get_month(day):
    """Return the json for the month"""
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    start_of_month = day_date.replace(day=1)  # First day of the month
    end_of_month = (start_of_month + datetime.timedelta(days=32)).replace(day=1)\
                                - datetime.timedelta(days=1)  # Last day of the month


    classes_subquery = get_class_of_user()

    insa_classes = (
        get_joined_class_subquery().filter(
            InsaClass.id.in_(classes_subquery),
            InsaClass.date.between(start_of_month, end_of_month)  # Filter for the entire week
        )
        .all()
    )

    return get_json_output(insa_classes)

@api.route('is_connected',methods =["GET"])
def get_is_connected():
    return jsonify({"is_connected":current_user.is_authenticated});


@api.route('get_year/<string:day>',methods =["GET"])
@login_required
def get_year(day):
    """Return the json for the year """
    day_date = datetime.datetime.strptime(day, "%Y-%m-%d")

    start_of_year = day_date.replace(month=1,day=1)  # First day of the year
    end_of_year = (start_of_year + datetime.timedelta(days=400)).replace(day=1,month=1)\
                                - datetime.timedelta(days=1)  # Last day of the year


    classes_subquery = get_class_of_user()

    insa_classes = (
        get_joined_class_subquery().filter(
            InsaClass.id.in_(classes_subquery),
            InsaClass.date.between(start_of_year, end_of_year)  # Filter for the entire year
        )
        .all()
    )

    return get_json_output(insa_classes)


@api.route('/fetch')
@login_required
def fetch():
    """ TEMPORARY FUNCTION SHOULD BE USED CAREFULLY PROBABLY"""
    if current_user.admin :
        list_of_records = fetch_entire_year("2024", "ITI", "3")
        insert_list_record(db.session, list_of_records)
        return "successfully fetched"

    return render_template('404_Not_Found.html')


@api.route('/enums/<enum_name>',methods =["GET"])
def get_enums(enum_name):
    model_mapping = {
        "type": EnumType,
        "sector": EnumSector,
        "color": EnumColor
    }
    
    model = model_mapping.get(enum_name.lower())
    if not model:
        return jsonify({"error": "Invalid enum type"}), 400

    if enum_name.lower() == "color":
        enums = [{"value": c.value, "label": c.user_friendly_name} for c in model.query.all()]
    else:
        enums = [{"value": e.name, "label": e.name} for e in model.query.all()]

    return jsonify(enums)



def get_joined_class_subquery():
    """ return the joined table subquery """
    return db.session.query(InsaClass).options(
            joinedload(InsaClass.link_td),
            joinedload(InsaClass.link_teacher),
            joinedload(InsaClass.link_room),
            joinedload(InsaClass.link_depart),
        )


def get_class_of_user():
    """transform the user tags to a classes_subquery"""
    tags_subquery = db.session.query(UserLinkTD.name_td)\
                    .filter_by(user_id=current_user.id).subquery() #current_user.id

    return db.session.query(ClassLinkTD.class_id)\
                    .filter(ClassLinkTD.td_id.in_(tags_subquery)).subquery()

def get_json_output(insa_classes):
    """transform the insa_class object in insa_class into a json for the front"""
    return jsonify([
        {
            "date": insa_class.date.strftime("%Y-%m-%d"),
            "start": insa_class.start_hour.strftime('%H%M'),
            "end": insa_class.end_hour.strftime('%H%M'),
            "desc": insa_class.desc,
            "td": [td.td.name for td in insa_class.link_td],
            "teacher": [teacher.teacher.name for teacher in insa_class.link_teacher],
            "room": [room.room.name for room in insa_class.link_room]
        }
        for insa_class in insa_classes
    ])
    
    