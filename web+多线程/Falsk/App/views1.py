from flask import Blueprint,url_for,render_template,request,Response,redirect
from .models import Person,db
import random

blue = Blueprint('two_blue',__name__) #取名称

@blue.route('/2')
def hello_world():
    return "Hello World,我是蓝图，可拆分多个222222"

@blue.route('/createdb/')
def create_db():
    db.create_all()
    return 'DB Create Success'

@blue.route('/addperson/')
def add_person():
    p =Person()
    p.p_name = "睡着了%d秒"%random.randrange(1000)
    db.session.add(p)
    db.session.commit()
    return 'Person Add Success'

@blue.route('/getpersons/')
def get_persons():
    persons = Person.query.all()
    # for person in persons:
    #     print(person.p_name)
    # return person.p_name
    return render_template("index1.html" ,persons=persons)