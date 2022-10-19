from flask import Flask, jsonify, session, render_template, url_for, request, redirect, flash, make_response
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRF
from transfer import course_register, list_courses, courses_db, exist_user, user_register
from functools import wraps
from app import create_app
from app.models import ProductModel
from app.firestore_service import get_product, get_user_products, get_users, get_products, product_put
import unittest
import datetime, jwt
import copy

app = create_app()

csrf = CSRFProtect()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    response = make_response(redirect('/home'))
    return response


@app.route('/home')
def home():
    user_ip = session.get('user_ip')
    username = current_user
    context = {
        'user_ip' : user_ip,
        'username' : username,
        #'product' : get_product(user_id=username)
    }

    users = get_users()
    #print(context['product'].to_dict())
    return render_template('home.html') 


@app.route('/courses', methods = ['GET'])
def courses_list():
    json_courses = list_courses(db)
    return json_courses


@app.route('/courses', methods = ['POST'])
@csrf.exempt
def courses_register():
    json_register = course_register(db)
    return json_register


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@app.route('/productos', methods=['GET', 'POST'])
def productos():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
            'user_ip' : user_ip,
            'username' : username,
            'products' : get_products()
        }
    # for product in context['products']:
    #     print(product.to_dict()['category'])
    return render_template('productos.html', **context)


@app.route('/add_to_cart/<string:product_id>')
@login_required
def add_to_cart(product_id):
    user_ip = session.get('user_ip')
    username = current_user.id
    product_model = ProductModel(username, product_id)
    product_put(product_model)
    context = {
        'user_ip': user_ip,
        'username': username,
    }
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    user_ip = session.get('user_ip')
    username = session.get('username')
    products = []
    if current_user.is_authenticated:
        username = current_user.id
        #Devuelve la cant de clicks en Comprar que hizo un usuario en un producto
        user_products = get_user_products(username)
        products = []
        for user_product in user_products:
            product_id = user_product.to_dict()['product']
            product = get_product(product_id)
            products.append(copy.copy(product))
            print(product.to_dict()['name'])

    context = {
        'user_ip': user_ip,
        'username': username,
        'user_products' : products
    }
    
    
    return render_template('cart.html', **context)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/product-page')
def product_desc():
    return render_template('product-page.html')


@app.route('/list', methods = ['GET'])
@login_required
def list():
    courses = courses_db(db)
    return render_template('list.html', courses = courses)


def status_401(error):
    return redirect(url_for('auth.login'))


def status_404(error):
    return "<h1>Página no encontrad</h1>"


if __name__ == "__main__":
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
