class Config:
    SECRET_KEY = 'KeyUltraSecreta$123'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'login'


config = {
    'development' : DevelopmentConfig
}
