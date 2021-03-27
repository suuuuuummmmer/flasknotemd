from datetime import datetime

from flask import url_for, redirect, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.urls import url_parse

from app import db, app
from app.forms import InputForm, LoginForm, RegistrationForm
from app.models import Todo, Comment, User



@app.route('/', methods=["GET", "POST"])
@app.route('/index/')
@login_required
def index():

    tasks = Todo.query.order_by(Todo.date_created).all()
    title = 'Task Index'

    # if request.method == "POST":
    #     task_content = request.form['content']
    #     new_task = TodoTodo(content=task_content)
    form = InputForm()
    if form.validate_on_submit():
        new_task = Todo(content=form.task.data, creator=form.creator.data, assignee=form.assign.data,
                        status=form.status.data, plan_endtime=form.endtime.data)
        # try:
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
        # except:
        #     return 'there was an issue adding your task.'

    else:

        return render_template('index.html', tasks=tasks, form=form, title=title)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    comments = Comment.query.filter(Comment.todo_id == task_to_delete.id)
    try:
        db.session.delete(task_to_delete)
        for comment in comments:
            db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'there was a problem deleting task'


# @app.route('/delete/<int:id>')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    title = 'Update Info'
    task = Todo.query.get_or_404(id)
    comments = Comment.query.filter(Comment.todo_id == task.id)
    # # form = UpdateForm()
    # # if form.validate_on_submit():
    #     new_task = TodoTodo(content=form.task.data, creator=form.creator.data, assignee=form.assign.data,
    # #                         status=form.status.data, endtime=form.endtime.data)
    #     try:
    #     db.session.add(new_task)
    #     db.session.commit()
    #     return redirect(url_for('index'))
    # except:
    #     return 'there was an issue adding your task.'
    if request.method == 'POST':
        task.content = request.form['content']
        # task.creator = request.form['creator']
        task.assignee = request.form['assignee']
        task.status = request.form['status']
        task.update_time = datetime.utcnow()
        task.plan_endtime = request.form['endtime']
        if request.form['comment']:
            comment = Comment(body=request.form['comment'], todo_id=task.id)
            db.session.add(comment)
        try:

            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task, comments=comments, title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Sign In'
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('账号或密码错误')
            return render_template(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)  # , email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('login'))
    return render_template('register.html', title=title, form=form)

#
