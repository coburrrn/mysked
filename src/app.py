import os
from flask import Flask, render_template
from src.common.database import Database

__author__ = 'dsmith'

app = Flask(__name__)
app.config.from_object('config')
#app.secret_key = "123"
app.secret_key = os.environ.get("SECRET_KEY")

@app.before_first_request
def init_db():
    Database.init()

@app.route("/")
def home():
    return render_template("home.html")

from src.models.users.views import user_blueprint
from src.models.sked.views import sked_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(sked_blueprint, url_prefix="/sked")




