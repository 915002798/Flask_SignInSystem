# -*- coding: utf-8 -*-
# @Version  : 1.0
# @Author   :

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
import pymysql
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/sign_in_system"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = os.urandom(24)       # 设置SECRET_KEY

'''
app.config["REDIS_URL"] = "redis://192.168.4.1:6379/0"
'''

app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")  # 文件上传
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")
app.debug = True

db = SQLAlchemy(app)
rd = FlaskRedis(app)

from app.admin import admin as admin_blueprint
from app.student import student as student_blueprint
from app.teacher import teacher as teacher_blueprint

app.register_blueprint(student_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(teacher_blueprint, url_prefix="/teacher")


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
# @app.route('/')
# def func():
#     return render_template('title.html')


'''
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
'''