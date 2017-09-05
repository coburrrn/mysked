
from flask import Blueprint, request, render_template, session, url_for
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
import src.models.users.decorators as decorators
from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_sked"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("/users/login.html")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        try:
            if User.register_user(email, password, name):
                session['email'] = email
                return redirect(url_for('.user_sked'))
        except UserErrors.UserError as e:
            return e.message
    return render_template("/users/register.html")

@user_blueprint.route('/sked')
@decorators.requires_login
def user_sked():
    user = User.find_by_email(session['email'])
    skeds = user.get_sked()
    return render_template('users/sked.html', skeds=skeds, user_name=user.name)

@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))
