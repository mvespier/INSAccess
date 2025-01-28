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
from app.models import User

parameters = Blueprint('parameters', __name__)

