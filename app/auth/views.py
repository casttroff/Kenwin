from flask import render_template, flash, request, session, url_for, redirect
from werkzeug.security import generate_password_hash
from . import auth
from app.firestore_service import get_user, user_put
# Entities
from app.forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import UserModel, UserData


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if password_from_db == password:
                print(user_doc.id)
                print(user_doc.to_dict()['password'])
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                return redirect(url_for('index'))
            else:
                flash('Contraseña incorrecta')
                render_template('auth/login.html', **context)
        else:
            flash('El usuario no existe')
        render_template('auth/login.html', **context)
    return render_template('auth/login.html', **context)


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form' : signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Registrado con éxito')

            return redirect(url_for('home'))
        else:
            flash("El usuario ya existe")
    return render_template('signup.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))
