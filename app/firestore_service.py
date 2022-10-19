import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential, {'projectId' : 'mywebsite-365407'})

db = firestore.client()

def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password' : user_data.password})


def get_products():
    return db.collection('products').get()


def get_product(product_id):
    return db.collection('products').document(product_id).get()


def get_user_products(user_id):
    return db.collection('users')\
        .document(user_id)\
        .collection('products').get()


def product_put(product_data):
    user_ref = db.collection('users').document(product_data.username).collection('products')
    user_ref.add({'product' : product_data.product})







