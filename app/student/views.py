import time
import uuid

from functools import wraps
from flask import render_template, redirect, url_for, session, request
from wtforms.validators import ValidationError
from werkzeug.security import generate_password_hash
from . import student
from app import db, app
from app.models import Student, Class, Sign
from app.student.forms import LoginForm, RegisterForm, SignForm



# 登陆装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for("student.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def hello_world():
    return redirect(url_for('student.login'))


# 登录
@student.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # 通过session获取 error_message
    error_message = session.get('error_message')
    session["error_message"] = None

    if request.method == "POST":
        data = form.data
        user = Student.query.filter_by(username=data["username"]).first()

        if not user:
            error_message = "用户名不存在！"
            session["error_message"] = error_message
            return redirect(url_for("student.login"))
        if not user.check_pwd(data["pwd"]):
            error_message = "密码错误！"
            session["error_message"] = error_message
            return redirect(url_for("student.login"))

        session["username"] = user.username
        return redirect(url_for("student.sign"))

    return render_template("student/login.html", form=form, error_message=error_message)


# 登出
@student.route('/logout/')
def logout():
    session["username"] = None
    return redirect(url_for("student.login"))


# 注册
@student.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    classes = Class.query.all()

    if request.method == "POST":
        # 获取数据
        form = RegisterForm(request.form)

        try:
            form.validate_name(form.username)
            form.validate_email(form.email)
            form.validate_phone(form.phone)
            form.validate_sid(form.sid)
        except ValidationError as e:
            context = {
                'err': None,
                'err2': e,
            }
            err2 = None
            return render_template("student/register.html", form=form, **context)

        if form.validate():
            data = form.data
            stu = Student(
                id=data["sid"],
                username=data["username"],
                name=data["name"],
                sex=data["sex"],
                pwd=generate_password_hash(data["pwd"]),
                cid=data["cls"],
                email=data["email"],
                phone=data["phone"],
                birthday=data["birthday"],
                date_in=data["date_in"],
                uuid=uuid.uuid4().hex
            )
            db.session.add(stu)
            db.session.commit()
            return render_template("student/register_ok.html")

    err = form.errors
    context = {
        'err': err,
        'err2': None,
    }
    err = None
    return render_template("student/register.html", form=form, classes=classes, **context)


# 查看所有班级
@student.route("/class/")
def all_class():
    data = Class.query.all()
    return render_template("student/class.html", data=data)


# 忘记密码
@student.route("/reset_password/")
def reset_password():
    pass
    # data = Class.query.all()
    # return render_template("student/forgot-password.html", data=data)


# 学生签到页面
@student.route("/sign/", methods=["GET", "POST"])
@student.route("/sign/<int:page>", methods=["GET", "POST"])
@user_login_req
def sign(page=1):
    form = SignForm()
    username = session.get("username")
    user = Student.query.filter_by(username=username).first()
    datetime = time.strftime('%Y-%m-%d %H:%M:%S')
    sid = user.id
    sign = Sign.query.filter_by(sid=sid).all()
    pager = Sign.query.filter_by(sid=sid).paginate(page, 10)

    if request.method == "GET":

        context = {
            'form': form,
            'user': user,
            'sign': sign,
            'datetime': datetime,
            'sign_count': len(sign),
            'pager': pager,
        }

        return render_template("student/sign.html", **context)

    elif request.method == "POST":
        form = SignForm(request.form)
        data = form.data

        do_sign = Sign(
            sid=sid,
            unit=data["unit"],
            v_num=data["v_num"],
            code_num=data["code_num"],
            operation=True
        )
        db.session.add(do_sign)
        db.session.commit()
        return redirect(url_for("student.sign"))


# **************************************** 测试Ajax用 ******************************************
# 注册--Ajax校验版
from flask import jsonify


@app.route("/userValid/", methods=['GET', 'POST'])
def userValid():
    # 定义json字典数据格式
    result = {
        "code": "",
        "data": ""
    }
    if request.method == "POST":
        # 获取ajax请求中的参数
        username = request.args.get("username")
        if username:
            # 查询数据库有无这个用户
            user = Student.query.filter_by(username=username).first()
            if user:
                result["code"] = 400
                result["data"] = "用户名已存在"
            else:
                result["code"] = 200
                result["data"] = "用户名未被注册，可以使用"
        return jsonify(result)
