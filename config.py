import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:670825@localhost:3306/blog'
    FLASKY_COMMENT_PER_PAGE = 7
    FLASKY_POST_PER_PAGE = 5
    UPLOAD_FOLDER = r'C:\Users\12\PycharmProjects\Blog-bootstrap\app\static\upload'
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

    @staticmethod
    def init_app(app):
        pass

config = {'default': Config}
