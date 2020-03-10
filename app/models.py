from datetime import datetime
from sqlalchemy import DateTime

# from app import db

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/sign_in_system"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


# ################################################## 前台 #################################################
# 班级表
class Class(db.Model):
    __tablename__ = "class"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True, nullable=False)  # 班级名

    def __repr__(self):
        return "<Class %r>" % self.name


# 学生信息表
class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)  # 学生ID
    username = db.Column(db.String(100), unique=True, nullable=False)  # 用户名
    name = db.Column(db.String(100), nullable=False)  # 学生姓名
    pwd = db.Column(db.String(100))  # 密码
    cid = db.Column(db.ForeignKey("class.id"), nullable=False)  # 所属班级
    sex = db.Column(db.Integer)  # 学生性别
    # birthday = db.Column(db.DateTime)  # 生日
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    # date_in = db.Column(db.Date, nullable=False)  # 入学时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符

    cls = db.relationship("Class", backref="student")  # 学生与班级外键关联关系

    def __repr__(self):
        return "<Student %r>" % self.username

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 教师信息表
class Teacher(db.Model):
    __tablename__ = "teacher"

    id = db.Column(db.Integer, primary_key=True)  # 教师ID
    username = db.Column(db.String(100), unique=True, nullable=False)  # 用户名
    name = db.Column(db.String(100), nullable=False)  # 教师姓名
    pwd = db.Column(db.String(100))  # 密码
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    email = db.Column(db.String(100), unique=True)  # 邮箱

    def __repr__(self):
        return "<Teacher %r>" % self.username

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 签到表
class Sign(db.Model):
    __tablename__ = "sign"

    id = db.Column(db.Integer, primary_key=True)  # 编号
    sid = db.Column(db.Integer)  # 学生ID
    datetime = db.Column(DateTime, nullable=False, default=datetime.now)
    unit = db.Column(db.String(100))  # 章节
    v_num = db.Column(db.Integer)  # 视频号
    code_num = db.Column(db.Integer)  # 代码量
    operation = db.Column(db.String(20))  # 操作
    text = db.Column(db.String(200))  # 备注

    __mapper_args__ = {
        "order_by": datetime.desc()  # 指定排序方式为倒序
    }

    def __repr__(self):
        return "<Sign %s,%s>" % (self.sname, self.date)


# ################################################ 后台 ####################################################
# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 角色权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship("Oplog", backref='admin')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


# ############################### 测试添加数据 #################################

# if __name__ == "__main__":
#     db.drop_all()
#     db.create_all()
#     cls1 = Class(id=401, name="Python 班")
#     cls2 = Class(id=402, name="Java 班")
#     db.session.add_all([cls1, cls2])
#     db.session.commit()

'''
    role = Role(
        name="超级管理",
        auths="1"
    )
    db.session.add(role)
    db.session.commit()

    # 哈希加密密码
    from werkzeug.security import generate_password_hash

    admin = Admin(
        name="superAdmin",
        pwd=generate_password_hash("superAdmin"),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
'''
