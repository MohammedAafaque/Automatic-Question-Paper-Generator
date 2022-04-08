from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

from website.models import Semester, Subject

views = Blueprint('views', __name__)



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