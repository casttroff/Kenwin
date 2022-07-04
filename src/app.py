from flask import Flask, jsonify, render_template, url_for, request, redirect, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRF
from transfer import course_register, list_courses, courses_db
from config import config
from functools import wraps
import datetime, jwt
import jyserver.Flask as jsf

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()

db = MySQL(app)

login_mannager = LoginManager(app)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)
    return decorator


@login_mannager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def Index():
    return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user:
            if logged_user.password:
                login_user(logged_user)
                token = jwt.encode({'public_id': logged_user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=20)}, app.config['SECRET_KEY']).decode('utf-8')
                print(token)
                return redirect(url_for('home'))
            else:
                flash('Invalid password')
                return render_template('auth/login.html')
        else:
            flash('User not found')
            return render_template('auth/login.html')
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/courses', methods = ['GET'])
@token_required
def courses_list():
    json_courses = list_courses(db)
    return json_courses


@app.route('/courses', methods = ['POST'])
@csrf.exempt
@token_required
def courses_register():
    json_register = course_register(db)
    return json_register


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/list', methods = ['GET'])
@login_required
def list():
    courses = courses_db(db)
    return render_template('list.html', courses = courses)


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrad</h1>"


if __name__ == "__main__":
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
