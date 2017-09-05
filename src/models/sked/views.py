from flask import Blueprint, render_template, request, session, url_for
from werkzeug.utils import redirect

import src.models.users.decorators as decorators
from src.models.sked.sked import Sked

sked_blueprint = Blueprint('skeds', __name__)

@sked_blueprint.route('/new', methods=['GET','POST'])
@decorators.requires_login
def add_sked():
    if request.method == 'POST':
        name = request.form['name']
        day = request.form['day']
        time = request.form['time']
        sked = Sked(session['email'], day, time, name)
        sked.save()
    return render_template('skeds/add_sked.html')

@sked_blueprint.route('/edit/<string:sked_id>', methods=['GET','POST'])
@decorators.requires_login
def edit_sked(sked_id):
    sked = Sked.find_by_id(sked_id)
    if request.method == "POST":
        name = request.form['name']
        day = request.form['day']
        time = request.form['time']
        sked.day = day
        sked.time = time
        sked.name = name
        sked.save()
        return redirect(url_for('users.user_sked'))
    return render_template('skeds/edit_sked.html', sked=sked)

@sked_blueprint.route('/delete/<string:sked_id>')
@decorators.requires_login
def delete_sked(sked_id):
    Sked.find_by_id(sked_id).delete()
    return redirect(url_for('users.user_sked'))

