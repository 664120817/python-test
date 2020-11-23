from flask import Flask,render_template,request
import datetime,uuid
app = Flask(__name__)

@app.route('/user/<name>/')#默认为str <name>= 传入的变量 <int:id>整数  folat 浮点   path 能将/认为字符 不转化
def welcome(name='gfgf' ,ooo = 'girl'): #参数允许有默认值ooo =girl
    print(name,ooo)
    return 'Hello World,%s,%s'%(name,ooo)

@app.route('/')  #访问路径
def hello_world2():   #网页传入变量
    time = datetime.date.today()
    name = ["小王","小明","小红","小亮"] #列表类型
    task = {"任务":"打扫卫生","时间":"3个小时"} #字典类型
    return render_template('index.html',var =time ,list = name, dict =task)
@app.route('/getuuid/')
def get_uuid():
    print(uuid.uuid4())
    return str(uuid.uuid4())

@app.route('/test/register')  #表单提交
def register():
    return render_template("test/register.html")
@app.route('/test/result',methods =["POST","GET"]) #接收表单需要指定methods类型
def result():
    if request.method == "POST":
        result = request.form
        print(result)
        print(request.form.get('Name'))
        print (request.remote_addr) #IP获取
        return render_template("test/result.html",result=result)

#注册蓝图 结构拆分
from App.views import blue
from App.views1 import blue as blue1
app.register_blueprint(blueprint=blue)
app.register_blueprint(blueprint=blue1)
#创建数据库sqlite 数据库调用
from App.models import init_db
# app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///sqlite3.db'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:4786874@localhost:3306/jianshu1'

app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] =False
init_db(app)
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='127.0.0.1')

#前端模板 https://bootstrapmade.com          https://v3.bootcss.com/
# https://colorlib.com/wp/templates/
#https://colorlib.com/wp     https://colorlib.com/wp/
#https://startbootstrap.com/themes/sb-admin-2/

