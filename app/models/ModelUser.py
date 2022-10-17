from flask_login import LoginManager
from .entities.User import User

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = %s """
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, fullname FROM user 
                    WHERE id = %s """
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)