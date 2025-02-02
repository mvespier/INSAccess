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


admin = Blueprint('admin', __name__,url_prefix='/admin/')

def admin_required(func):
    
    def func_404():
        return render_template('404_Not_Found.html')

    def wrapper():
        if current_user.admin : 
            return func()
        else :
            return func_404()
        

    return wrapper

@admin.route('/association/', methods = ['GET'])
@admin_required
@login_required
def association_register():
    """ render the association creator"""
    return render_template('association.html')


 

@admin.route('/association/', methods = ['POST'])
@login_required
def create_association():
    """ Create an association in the website"""
    if current_user.admin :
        request_dict = request.form
        name = request_dict.get('name')
        return "success"

    return render_template('404_Not_Found.html')

