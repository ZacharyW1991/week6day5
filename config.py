import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY='blah'
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'app.db')