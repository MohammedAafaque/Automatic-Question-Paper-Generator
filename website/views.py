from typing import Optional
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from . import db
import json

from website.models import Semester, Subject, Module, Question, Subquestion, Template, Subquestiondetails

views = Blueprint('views', __name__)

@views.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    else:
        return render_template("landing.html", user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)
    

@views.route('/semester', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        sem = request.form.get('sem')

        if len(sem) < 1:
            flash('Semester is should be of at least 1 character.', category='error')
        else:
            new_sem = Semester(sem=sem, user_id=current_user.id)
            db.session.add(new_sem)
            db.session.commit()
            flash("Semester added successfully!", category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-sem', methods=['POST'])
def delete_sem():
    sem = json.loads(request.data)
    semId = sem['semId']
    sem = Semester.query.get(semId)
    if sem:
        if sem.user_id == current_user.id:
            db.session.delete(sem)
            db.session.commit()
    return jsonify({})

@views.route('/update-sem', methods=['POST'])
def update_sem():
    newSem = json.loads(request.data)
    semId = newSem['semId']
    updatedField = newSem['updatedSem']
    sem = Semester.query.get(semId)
    if sem:
        if sem.user_id == current_user.id:
            sem.sem = updatedField
            db.session.commit()
    return jsonify({})

@views.route('/semester/<semId>', methods=['GET', 'POST'])
@login_required
def subjects(semId):
    if request.method == 'POST':
        subject = request.form.get('sub')
        if len(subject) < 2:
            flash('Subject name should be of at least 2 characters.', category="error")
        else:
            new_sub = Subject(subject_ame=subject, semester_id=semId)
            db.session.add(new_sub)
            db.session.commit()
            flash("Subject added successfully!", category='success')

    sem = Semester.query.filter_by(id=semId).first()
    return render_template("subjects.html", sem=sem, user=current_user)

@views.route('/delete-sub', methods=['POST'])
def delete_sub():
    sub = json.loads(request.data)
    subId = sub['subId']
    sub = Subject.query.get(subId)
    if sub:
            db.session.delete(sub)
            db.session.commit()
    return jsonify({})

@views.route('/update-sub', methods=['POST'])
def update_sub():
    newSub = json.loads(request.data)
    subId = newSub['subId']
    updatedField = newSub['updatedSub']
    sub = Subject.query.get(subId)
    if sub:
            sub.subject_ame = updatedField
            db.session.commit()
    return jsonify({})

@views.route('/semester/<semId>/<subId>', methods=['GET', 'POST'])
@login_required
def modules(semId, subId):
    if request.method == 'POST':
        module = request.form.get('mod')
        if len(module) < 1:
            flash('Module name should be of at least 1 character.', category="error")
        else:
            new_mod = Module(module_name=module, subject_id=subId)
            db.session.add(new_mod)
            db.session.commit()
            flash("Module added successfully!", category='success')

    sub = Subject.query.filter_by(id=subId).first()
    sem = Semester.query.filter_by(id=semId).first()
    return render_template("modules.html", user=current_user, sub=sub, sem=sem)

@views.route('/delete-mod', methods=['POST'])
def delete_mod():
    mod = json.loads(request.data)
    modId = mod['modId']
    mod = Module.query.get(modId)
    if mod:
            db.session.delete(mod)
            db.session.commit()
    return jsonify({})

@views.route('/update-mod', methods=['POST'])
def update_mod():
    newMod = json.loads(request.data)
    modId = newMod['modId']
    updatedField = newMod['updatedMod']
    mod = Module.query.get(modId)
    if mod:
            mod.module_name = updatedField
            db.session.commit()
    return jsonify({})

@views.route('/semester/<semId>/<subId>/<modId>', methods=['GET', 'POST'])
@login_required
def questions(semId, subId, modId):
    if request.method == 'POST':
        question = request.form.get('question')
        if len(question) < 4:
            flash('Question should be of at least 4 characters.', category="error")
        else:
            new_ques = Question(question_content=question, module_id=modId)
            db.session.add(new_ques)
            db.session.commit()
            flash("Question added successfully!", category='success')

    mod = Module.query.filter_by(id=modId).first()
    sub = Subject.query.filter_by(id=subId).first()
    sem = Semester.query.filter_by(id=semId).first()
    return render_template("questions.html", user=current_user, mod=mod, sub=sub, sem=sem)

@views.route('/delete-question', methods=['POST'])
@login_required
def delete_question():
    ques = json.loads(request.data)
    quesId = ques['quesId']
    ques = Question.query.get(quesId)
    if ques:
            db.session.delete(ques)
            db.session.commit()
    return jsonify({})

@views.route('/update-question', methods=['POST'])
@login_required
def update_question():
    newQues = json.loads(request.data)
    quesId = newQues['quesId']
    updatedField = newQues['updatedQuestion']
    ques = Question.query.get(quesId)
    if ques:
            ques.question_content = updatedField
            db.session.commit()
    return jsonify({})

@views.route('/generate')
@login_required
def generate():
    id = current_user.id
    sems = Semester.query.filter_by(user_id=id)
    return render_template("select_sem.html", user=current_user, sems=sems)

@views.route('/generate/<semId>')
@login_required
def showSubs(semId):
    subs = Subject.query.filter_by(semester_id=semId)
    return render_template("select_sub.html", user=current_user, subs=subs, semId=semId)

@views.route('/generate/<semId>/<subId>')
@login_required
def displayTemplates(semId, subId):
    temps = Template.query.filter_by(user_id=current_user.id)
    return render_template("displayTemplates.html", user=current_user, temps=temps, semId=semId, subId=subId)
    # temps = Template.query.filter_by(user_id=current_user.id)
    # return render_template("displayTemplates.html", user=current_user, temps=temps, semId=semId, subId=subId)

@views.route('/generate/<semId>/<subId>/create', methods=['GET', 'POST'])
@login_required
def createTemplate(semId, subId):
    if request.method == 'POST':
        user=current_user
        name = request.form.get('templateName')
        total = int(request.form.get('totalQuestions'))
        compulsory = int(request.form.get('compulsoryQuestions'))
        optional = int(request.form.get('optionalQuestions'))
        marks = int(request.form.get('marks'))

        if len(name)<1:
            flash("Template name should be of at least 1 character", category="success")
        # elif ((compulsory+optional) != total):
        #     flash("Total questions are not equal to compulsory & optional questions", category="error")
        else:    
            new_template = Template(name=name, totalQ=total, compulsoryQ=compulsory, optionalQ=optional, marks=marks,user_id=user.id )
            db.session.add(new_template)
            db.session.commit()
            return redirect(url_for('views.displayTemplates', semId=semId, subId=subId))

    sub = Subject.query.filter_by(id=subId).first()
    if sub:
        return render_template("formatInfo.html", sub=sub, user=current_user)

@views.route('/generate/<semId>/<subId>/<tempId>', methods=['POST', 'GET'])
@login_required
def addSubquestion(semId, subId, tempId):
    if request.method == 'POST':
        data = request.form
        question_dict = {}
        for key in data:
            new_question = Subquestion(question_number=key, subquestions=data[key], template_id=tempId)
            db.session.add(new_question)
            db.session.commit()
            question_dict[key] = new_question.id
        input = json.dumps(question_dict)
        return redirect(url_for('views.setTemplate', semId=semId, subId=subId, tempId=tempId, params=input))

    temp = Template.query.filter_by(id=tempId).first()
    compul = temp.compulsoryQ
    opt = temp.optionalQ
    if temp:
        return render_template("subQuestions.html", user=current_user, semId=semId, subId=subId, tempId=tempId, temp=temp, compul=compul, opt=opt)

@views.route('/generate/<semId>/<subId>/<tempId>/create/<params>', methods=['POST', 'GET'])
@login_required
def setTemplate(semId, subId, tempId, params):
    if request.method=='POST':
        dict = json.loads(params)
        modules = request.form.getlist('cMod')
        marks = request.form.getlist('cMarks')
        blooms = request.form.getlist('cCO')
        j=0
        for key in dict:
            ques = Subquestion.query.filter_by(id=dict[key]).first()
            subques = ques.subquestions
            for i in range(subques):
                new_subquestion = Subquestiondetails(module=modules[j], marks=marks[j], bloom=blooms[j], subquestion_of=dict[key])
                db.session.add(new_subquestion)
                db.session.commit()
                j=j+1
        return redirect(url_for('views.dashboard'))
        
    dict = json.loads(params)
    temp = Template.query.filter_by(id=tempId).first()
    sub = Subject.query.filter_by(id=subId).first()
    return render_template("setTemplate.html", user=current_user, subquestions=temp.subquestions, compulsory=temp.compulsoryQ, optional=temp.optionalQ, subject=sub)
