from flask_wtf import FlaskForm     # FlaskForm为表单基类
from wtforms.fields import SubmitField, StringField, PasswordField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError, InputRequired
from app.models import Teacher


class LoginForm(FlaskForm):
    username = StringField(
        label="用户名",
        validators=[
            DataRequired("请输入用户名！")
        ],
        description="用户名",
        render_kw={
            "class": "form-control",
            "id": "username",
            "placeholder": "请输入用户名！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "id": "password",
            "placeholder": "请输入密码！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-info",
        }
    )


class RegisterForm(FlaskForm):
    username = StringField(
        label="用户名",
        validators=[
            InputRequired(message="请输入用户名！"),
        ],
        description="用户名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户名！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )
    name = StringField(
        label="姓名",
        validators=[InputRequired(message="请输入姓名！")],
        description="姓名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入姓名！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[InputRequired(message="请输入密码！")],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[InputRequired(message="请输入确认密码！"), EqualTo('pwd', message="两次密码不一致！")],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入确认密码！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[InputRequired(message="请输入邮箱！"), Email(message="邮箱格式不正确！")],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )
    phone = StringField(
        label="手机号码",
        validators=[InputRequired(message="请输入手机号码！"), Regexp("1[3589]\\d{9}", message="手机号码格式不正确！")],
        description="手机号码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机号码！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )

    def validate_name(self, field):
        username = field.data
        user = Teacher.query.filter_by(username=username).count()
        if user == 1:
            raise ValidationError("用户名已经存在！")

    def validate_email(self, field):
        email = field.data
        user = Teacher.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在！")

    def validate_phone(self, field):
        phone = field.data
        user = Teacher.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机号码已经存在！")


class GetSignsForm(FlaskForm):
    pass