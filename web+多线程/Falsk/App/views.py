from flask import Blueprint,url_for,render_template,request,Response,redirect
blue = Blueprint('first_blue',__name__) #取名称

@blue.route('/1')
def hello_world():
    return "Hello World,我是蓝图，可拆分多个"

@blue.route('/urlfor/')
def urlfor():  #反向解析
    result = url_for('first_blue.hello_world') #要以蓝图名字调用
    return result

@blue.route('/APP_test/home/')
def home():
    cookies = request.cookies.get('cookie') #获取cookie 并发出去
    return render_template('/APP_test/home.html',cookies = cookies)

@blue.route('/APP_test/login/',methods =['GET','POST'])
def login():
    if request.method =="GET":
        return render_template('/APP_test/login.html')
    elif request.method == "POST":
        user =request.form.get('user')
        print(user)
        resp = Response(response="%s，登陆成功！"%user)
        resp.set_cookie('cookie',user +'！ 可查看我的cookies') #设置cookie
        return resp
@blue.route('/logout/')
def logout():
    resp = redirect(url_for('first_blue.home'))
    resp.delete_cookie('cookie')
    return resp


#魔法语法 结构标签
@blue.route('/结构标签1/')
def base1():
    return render_template('/APP_test/继承结构标签1.html')

@blue.route('/结构标签2/')
def base2():
    return render_template('/APP_test/继承结构标签2.html')