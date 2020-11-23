#数据库调用
from flask_sqlalchemy import SQLAlchemy

db =SQLAlchemy()
def init_db(app):
    db.init_app(app)

class Person(db.Model):  # Person 是表名

    p_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    p_name =  db.Column(db.String(16))


