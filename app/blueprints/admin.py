"""
Module Name: admin.py

Description:
    The blueprint for all special management route
    accessed only by admin

Author:
    Raphael Senellart

Date Created:
    January 30, 2025

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
from sqlalchemy.orm import joinedload
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from ..utils.decorator import admin_required


admin = Blueprint('admin', __name__,url_prefix='/admin/')

# @admin.before_request
# def admin_required():
#     if current_user.admin : 
#         return 
#     else :
#         return render_template('404_Not_Found.html')


@admin.route('/', methods = ['GET'])
@admin_required
@login_required
def association_register():
    """ render the association creator"""
    return render_template('admin.html')


@admin.route('/', methods = ['POST'])
@admin_required
@login_required
def create_association():
    """ Create an association in the website"""

    request_dict = request.form
    name = request_dict.get('name')
    return "success"

