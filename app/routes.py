from app import app, db
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SubmitForm, LoginForm, SignUpForm
from app.models import Address, User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submission():
    form=SubmitForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        first_name=form.first_name.data
        last_name=form.last_name.data
        phone=form.phone.data
        address=form.address.data
        new_address=Address(first_name=first_name, last_name=last_name, phone=phone, address=address, user_id=current_user.id)
        db.session.add(new_address)
        db.session.commit()
        flash("A new address has been entered")
        return redirect(url_for('index'))
    return render_template('submit.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
        if check_user:
            flash('A user with that username and/or email already exists')
            return redirect(url_for('signup'))
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        flash(f"{new_user.username} has been created!")

        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = db.session.execute(db.select(User).where(User.username==username)).scalar()
        if user is not None and user.check_password(password):
            login_user(user, remember=remember_me)
            flash(f'{user.username} has succesfully logged in.')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('index'))