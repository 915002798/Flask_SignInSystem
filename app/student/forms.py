from flask_wtf import FlaskForm  # FlaskForm为表单基类
from wtforms import validators
from wtforms.fields import SubmitField, StringField, PasswordField, SelectField, RadioField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError, InputRequired
from app.models import Student, db, Class


class SelectField2(SelectField):

    def pre_validate(self, form):
        pass


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
    pwd = PasswordField(
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
            InputRequired(message="请输入用户名！")
        ],
        description="用户名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户名！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )

    sex = RadioField(
        label="性别",
        choices=(('0', '男'), ('1', '女')),
        description="性别",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择性别！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        },

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
    sid = StringField(
        label="学号",
        validators=[InputRequired(message="请输入学号！")],
        description="学号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入学号！",
            "required": 'required',  # 表示此项不能为空
            "autofocus": "autofocus",
        }
    )

    l_cls = [(cls.id, cls.name) for cls in db.session.query(Class).all()]

    cls = SelectField2(
        coerce=str,
        label="班级",
        validators=[DataRequired('请选择班级')],
        choices=tuple(l_cls),
        render_kw={
            'class': 'form-control',
            "placeholder": "请选择班级！",
            "required": 'required',  # 表示此项不能为空
        },
    )
    birthday = DateTimeField(
        label="生日",
        validators=[InputRequired(message="请选择生日！")],
        description="生日",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择生日！",
            "autofocus": "autofocus",
        }
    )
    date_in = DateTimeField(
        label="入学时间",
        validators=[InputRequired(message="请选择入学时间！")],
        description="入学时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择入学时间！",
            "autofocus": "autofocus",
        }
    )
    agree = BooleanField('是否同意服务条件和隐私策略！', [validators.InputRequired()])

    def validate_name(self, field):
        username = field.data
        user = Student.query.filter_by(username=username).count()
        if user == 1:
            raise ValidationError("用户名已经存在！")

    def validate_email(self, field):
        email = field.data
        user = Student.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在！")

    def validate_phone(self, field):
        phone = field.data
        user = Student.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机号码已经存在！")

    def validate_sid(self, field):
        sid = field.data
        user = Student.query.filter_by(id=sid).count()
        if user == 1:
            raise ValidationError("学号已经存在！")


class SignForm(FlaskForm):
    unit = StringField(
        label="章节",
        validators=[
            DataRequired("请输入章节！"),
            Regexp(r'.+', message="请输入章节")
        ],
        description="章节",
        render_kw={
            "class": "form-control",
            "style": "width: 150px;height: 10px",
            "placeholder": "请输入章节！",
        }
    )
    v_num = StringField(
        label="视频号",
        validators=[
            DataRequired("请输入视频号！"),
            Regexp(r'^[1-9]\d*$', message="请输入视频号（数值型.例如:10,代表第10个视频。）")
        ],
        description="章节",
        render_kw={
            "class": "form-control",
            "style": "width: 150px;height: 10px",
            "placeholder": "请输入视频号！",
            "required": 'required',  # 表示此项不能为空
            # "required": False,  # 设置后，前端页面不进行required是否为空的校验。即点击提交后显示“请填写此字段！”不再显示
        }
    )
    code_num = StringField(
        label="章节",
        validators=[
            DataRequired("请输入代码数！"),
            Regexp(r'.+', message="请输入代码行数（数值型.例如:100，代表100行代码。）")
        ],
        description="代码数",
        render_kw={
            "class": "form-control",
            "style": "width: 150px;height: 10px",
            "placeholder": "请输入代码数！",
            "required": 'required',  # 表示此项不能为空
        }
    )
