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
from flask import current_app, Blueprint, render_template,\
                  redirect, url_for, request, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from ..models import InsaClass, User, UserLinkTD, ClassLinkTD,GroupTD, db
from sqlalchemy.orm import joinedload
from time import strftime


api = Blueprint('api', __name__)


@api.route('/api/get_week')
@login_required
def get_week():
    """return the json for the week"""
    tags = UserLinkTD.query.filter_by(user_id = current_user.id).all()
    tags_list = [tag.name_td for tag in tags]

    classes_insa = ClassLinkTD.query.filter(ClassLinkTD.td_id.in_(tags_list)).all()
    classes_list= [a_class.class_id for a_class in classes_insa]

    output =[]
    for i in classes_list:
        insa_class = db.session.query(InsaClass).options(
            joinedload(InsaClass.link_td),
            joinedload(InsaClass.link_teacher),
            joinedload(InsaClass.link_room),
            joinedload(InsaClass.link_depart),
        ).filter(InsaClass.id == i).first()

        dict = {
            "date" : insa_class.date.strftime("%Y-%m-%d"),
            "start" : insa_class.start_hour.strftime('%H:%M:%S'),
            "end" : insa_class.end_hour.strftime('%H:%M:%S'),
            "desc" : insa_class.desc,
            "td" : [td.td.name for td in insa_class.link_td]
        }

        output.append(dict)

    return jsonify(output)
