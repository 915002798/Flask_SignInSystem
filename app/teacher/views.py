from functools import wraps
from flask import render_template, redirect, url_for, session, request, jsonify
from werkzeug.security import generate_password_hash
from wtforms.validators import ValidationError

from . import teacher
from app import db, app
from app.models import Teacher, Class, Sign, Student
from app.teacher.forms import LoginForm, GetSignsForm, RegisterForm


# 登陆装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for("teacher.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@teacher.route('/')
def hello_world():
    return render_template('teacher/teacher-welcome.html')


@teacher.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    # 通过session获取 error_message
    error_message = session.get('error_message')
    session["error_message"] = None

    if request.method == "POST":
        data = form.data
        user = Teacher.query.filter_by(username=data["username"]).first()

        if not user:
            error_message = "用户名不存在！"
            session["error_message"] = error_message
            return redirect(url_for("teacher.login"))
        if not user.check_pwd(data["password"]):
            error_message = "密码错误！"
            session["error_message"] = error_message
            return redirect(url_for("teacher.login"))

        session["username"] = user.username

        return redirect(url_for("teacher.index"))

    return render_template("teacher/login.html", form=form, error_message=error_message)


@teacher.route('/logout/')
def logout():
    session["username"] = None
    return redirect(url_for("teacher.login"))


@teacher.route('/register/', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        form = RegisterForm()
        return render_template("teacher/register.html", form=form, err=None, err2=None)
    elif request.method == "POST":
        # 获取数据
        form = RegisterForm(request.form)
        try:
            form.validate_name(form.username)
            form.validate_email(form.email)
            form.validate_phone(form.phone)
        except ValidationError as e:
            return render_template("teacher/register.html", form=form, err=None, err2=e)

        if form.validate():
            data = form.data

            teacher = Teacher(
                username=data["username"],
                name=data["name"],
                pwd=generate_password_hash(data["pwd"]),
                email=data["email"],
                phone=data["phone"],
            )
            db.session.add(teacher)
            db.session.commit()

            session["username"] = teacher.username
            session["password"] = teacher.pwd
            return render_template("teacher/register_ok.html")
        err = form.errors
        return render_template("teacher/register.html", form=form, err=err, err2=None)


@teacher.route('/index/')
@user_login_req
def index():
    return render_template('teacher/index.html')


@teacher.route('/get_signs/', methods=["GET", "POST"])
@user_login_req
def get_signs():
    signs = Sign.query.with_entities(Sign.sid.label('sid'), Student.name.label('sname'), Class.name.label('cname'),
                                     Sign.datetime.label('datetime'), Sign.unit.label('unit'),
                                     Sign.v_num.label('v_num'), Sign.code_num.label('code_num')) \
        .join(Student, Sign.sid == Student.id).join(Class, Student.cid == Class.id).all()
    return render_template("teacher/get_signs.html", signs=signs)


@teacher.route('/search_sign/', methods=['POST'])
def search_sign():
    cname = request.form.get('cname')
    sname = request.form.get('sname')
    time = request.form.get('create_time')
    signs = Sign.query.with_entities(Sign.sid.label('sid'), Student.name.label('sname'), Class.name.label('cname'),
                                     Sign.datetime.label('datetime'), Sign.unit.label('unit'),
                                     Sign.v_num.label('v_num'), Sign.code_num.label('code_num')) \
        .join(Student, Sign.sid == Student.id).join(Class, Student.cid == Class.id)

    if time:
        signs = signs.filter(Sign.datetime.like(time + "%"))
    if sname:
        signs = signs.filter(Student.name == sname)
    if cname:
        signs = signs.filter(Class.name == cname)
    data = signs.all()
    datas = []
    for d in data:
        datas.append({
            'sid': d.sid,
            'sname': d.sname,
            'cname': d.cname,
            'datetime': str(d.datetime)[:11] if d.datetime else "",
            'unit': d.unit,
            'v_num': d.v_num,
            'code_num': d.code_num,
        })
    return jsonify({'data': datas})
