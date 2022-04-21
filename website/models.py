from . import db
from flask_login import UserMixin

# class Subquestion(db.Model):
#     id = db.Column(db.Integer, primary_key=True)


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    totalQ = db.Column(db.Integer)
    compulsoryQ = db.Column(db.Integer)
    optionalQ = db.Column(db.Integer)
    marks = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_content = db.Column(db.String(500))
    question_category = db.Column(db.Integer, default=0)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(200))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    questions = db.relationship('Question')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_ame = db.Column(db.String(200))
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'))
    mods = db.relationship('Module')

class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sem = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subs = db.relationship('Subject')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    institution_name = db.Column(db.String(150))
    department = db.Column(db.String(300))
    designation = db.Column(db.String(150))
    sems = db.relationship('Semester')
