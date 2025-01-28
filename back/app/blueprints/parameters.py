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
from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_required, current_user
from ..models import db, GroupTD, User, UserLinkTD

param = Blueprint('param', __name__, url_prefix='/param')

@param.route('/', methods=['GET'])
@login_required
def manage_td():
    user_tds = [link.name_td for link in current_user.link_td]
    all_tds = [td.name for td in GroupTD.query.all()]

    return render_template('td_selection.html', user_tds=user_tds, all_tds=all_tds)

@param.route('/', methods=['POST'])
@login_required
def manage_td_post():
    # Parse the submitted TD names
    selected_tds = request.json.get('selected_tds', [])

    # Clear existing links for the user
    UserLinkTD.query.filter_by(user_id=current_user.id).delete()

    # Add the new selected TDs
    for td_name in selected_tds:
        link = UserLinkTD(user_id=current_user.id, name_td=td_name)
        db.session.add(link)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Selections updated successfully.'})
