from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import StudentLeader, Issue
from forms import IssueForm, LoginForm, ResponseForm

@app.route('/')
def index():
    form = IssueForm()
    return render_template('index.html', form=form)

@app.route('/submit_issue', methods=['POST'])
def submit_issue():
    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(issue)
        db.session.commit()
        flash('Your issue has been submitted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = StudentLeader.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    issues = Issue.query.order_by(Issue.created_at.desc()).all()
    return render_template('dashboard.html', issues=issues)

@app.route('/update_issue/<int:issue_id>', methods=['POST'])
@login_required
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    action = request.form.get('action')
    
    if action == 'take':
        issue.handler_id = current_user.id
        issue.status = 'in_progress'
    elif action == 'resolve':
        issue.status = 'resolved'
    
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/respond/<int:issue_id>', methods=['POST'])
@login_required
def respond(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = ResponseForm()
    
    if form.validate_on_submit():
        issue.response = form.response.data
        db.session.commit()
        flash('Response submitted successfully', 'success')
    
    return redirect(url_for('dashboard'))
