# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:13:33 2020

@author: peter
"""
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import poem_generator


poem = poem_generator.rand_poem() #need to incorporate into recommend() path for first instantiation of variable 'poem'
recommend_num = 0 #need to replace this counter with making a list of 'skipped poems' to stop them from being recommended multiple times


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/recommend')
@login_required
def recommend():
    liked_poems_as_str = current_user.liked_poem_str
    if liked_poems_as_str != '':
        liked_poems = (liked_poems_as_str).split(',')
        number_of_liked_poems = len([int(num) for num in liked_poems])
    else:
        number_of_liked_poems = 0
    return render_template('recommend.html', title='recommend', poem = poem, number_of_liked_poems=number_of_liked_poems)

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    global poem
    global recommend_num
    poem_id = poem.name
    user = User.query.filter_by(username=current_user.username).first() #need to find shorter way to do this
    if user.liked_poem_str == '':
        user.liked_poem_str = str(poem_id)
    else:
        user.liked_poem_str = user.liked_poem_str + ',' + str(poem_id)
    db.session.commit()  
    recommend_num = 0
    return redirect(url_for('skip'))


@app.route('/skip', methods=['GET', 'POST'])
@login_required
def skip():
    global poem
    global recommend_num
    liked_poems_as_str = current_user.liked_poem_str
    if liked_poems_as_str == '':
        poem = poem_generator.rand_poem()
        return redirect(url_for('recommend'))
    liked_poems = (liked_poems_as_str).split(',')
    liked_poems = [int(num) for num in liked_poems]
    if len(liked_poems) < 10:
        poem = poem_generator.rand_poem()
    else:
        poem_id = poem_generator.recommend_poems(liked_poems)[recommend_num]
        poem = poem_generator.poem_info_from_id(poem_id)
        recommend_num += 1
    return redirect(url_for('recommend'))

@app.route('/random')
@login_required
def random():
    global poem
    poem = poem_generator.rand_poem()
    return redirect(url_for('recommend'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
    
    
