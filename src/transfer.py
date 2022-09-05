import code
from werkzeug.security import generate_password_hash
from flask import jsonify, request
from validations import code_validator, credit_validator, name_validator
from models.Courses import Course
import copy

def list_courses(db):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT code, name, credits FROM data ORDER BY name ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        courses = []
        for row in data:
            course = {'code': row[0], 'name': row[1], 'credits': row[2]}
            courses.append(course)
        return jsonify({'courses': courses, 'msj': "Cursos listados.", 'response': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def course_register(db):
    if (code_validator(request.json['code']) and name_validator(request.json['name']) and credit_validator(request.json['credits'])):
        try:
            curso = leer_curso_bd(db, request.json['code'])
            if curso != None:
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
            else:
                cursor = db.connection.cursor()
                sql = """INSERT INTO data (code, name, credits) 
                VALUES (%s, %s, %s)"""
                args = (request.json['code'], request.json['name'], request.json['credits'])
                cursor.execute(sql, args)
                db.connection.commit()
                return jsonify({'mensaje': "Curso registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


def leer_curso_bd(db, code):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT code, name, credits FROM data WHERE code = %s"
        cursor.execute(sql, (code, ))
        datos = cursor.fetchone()
        if datos != None:
            course = {'code': datos[0], 'name': datos[1], 'credits': datos[2]}
            return course
        else:
            return None
    except Exception as ex:
        raise ex


def courses_db(db):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT code, name, credits FROM data ORDER BY name ASC"
        cursor.execute(sql)
        data = cursor.fetchall()
        courses = []
        for row in data:
            course = Course(row[0], row[1],row[2])
            courses.append(copy.copy(course))
        return courses
    except Exception as ex:
        raise (ex)

def exist_user(db, user):
    try:
        cursor = db.connection.cursor()
        sql = "SELECT username FROM user WHERE username = %s"
        cursor.execute(sql, (user, ))
        username = cursor.fetchone()
        if username != None:
            return username
        else:
            return None
    except Exception as ex:
        raise ex


def user_register(db, user):
    try:
        cursor = db.connection.cursor()
        sql = "INSERT INTO user (id, username, password, fullname) VALUES (%s, %s, %s, %s)"
        password = generate_password_hash(user.password)
        args = (None, user.username, password, 'Hello')
        cursor.execute(sql, args)
        db.connection.commit()
    except Exception as ex:
        raise ex
