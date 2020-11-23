import time,re,pymysql,datetime

from application import urls
# 装饰器
def route(path):
    def function_out(func):
        urls.route_dict[path] = func
        def function_in():
            func()
        return function_in
    return function_out



@route("/index.py")
def index(n):
    #处理请求 index.py 请求
    db = pymysql.Connect(host="localhost", port=3306, user="root", passwd="4786874", db="spider", charset="utf8")
    cursor = db.cursor()
    # print(n)
    n = n.replace("=", ":")
    n=dict([item.split(":") for item in n.split("&")])
    # print(n)
    n=n["page"]
    num = int(n) * 100
    cursor.execute("select * from ttjj order by jzrq DESC,rzdf DESC limit {},100".format(num))
    # datas =str(cursor.fetchall())
    datas = """<table>
     <ol>
        <th>基金代码</th>
        <th>基金简称 </th>
        <th>最新日期</th>
        <th>单位净值</th>
        <th>累计净值</th>
        <th>今天涨幅</th>
        <th>一周涨幅</th>
        <th>一月涨幅</th>
        <th>三月涨幅</th>
        <th>六月涨幅</th>
        <th>一年涨幅</th>
        <th>二年涨幅</th>
        <th>三年涨幅</th>
        <th>今年来</th>
        <th>成立来</th>
        <th>手续费</th>
        <th>详情及购买</th>
    </ol>"""
    for data in cursor.fetchall():
        str = """                   
                            <tr>           
                           <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td><a href=%s target="_blank">查看</a></td>
                            </tr>
                            
                        """ %data

        datas += str
    cursor.close()
    db.close()
    s = """<div align="center">
          <a  class="next"  href="index.py"> 首页</a>
          <a  class="next"  href="index.py?page={}"> 下一页</a>
        </div>
        """.format(int(n) + 1)
    datas = datas + s

    with open("static/jj.html", "rb") as file:
        response_body = file.read()
        response_body = re.sub(r"{%content%}", datas+"</table>"+s, response_body.decode('utf-8'))
    return response_body
@route("/center.py")
def center(n):
    db = pymysql.Connect(host="localhost", port=3306, user="hao", passwd="4786874", db="spider", charset="utf8")
    cursor = db.cursor()
    n = n.replace("=", ":")
    n = dict([item.split(":") for item in n.split("&")])
    # print(n)
    n = n["page"]
    num=int(n)*100
    cursor.execute("select * from jjph order by date DESC,jz1 ASC limit {},100".format(num))
    # datas =str(cursor.fetchall())
    datas = """
    <table>
    <tr>
            <th>基金代码</th>
            <th>基金简称 </th>
            <th>一周排行</th>
            <th>一月排行</th>
            <th>三月排行</th>
            <th>六月排行</th>
            <th>今年排行</th>
            <th>一年排行</th>
            <th>二年排行</th>
            <th>三年排行</th>
            <th>今天日期</th>
            <th>同类总数</th>
            <th>详情</th>
       </tr>"""
    for data in cursor.fetchall():
        str = """
                            <tr>           
                              <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td><a href=%s target="_blank">详情</a></td>
                               </tr>

                           """ % data

        datas += str
    cursor.close()
    db.close()
    s="""<div align="center">
      <a  class="next"  href="center.py"> 首页</a>
      <a  class="next"  href="center.py&page={}"> 下一页</a>
    </div>
    """.format(int(n) + 1)
    datas = datas + s

    with open("static/jj.html", "rb") as file:
        response_body = file.read()
        response_body = re.sub(r"{%content%}", datas+"</table>"+s, response_body.decode('utf-8'))
    return response_body
@route("/meituan.py")
def meituan(n):
    # 处理请求 index.py 请求
    # return "This is gettime show {}".format(time.ctime())
    db = pymysql.Connect(host="localhost", port=3306, user="hao", passwd="4786874", db="spider", charset="utf8")
    cursor = db.cursor()
    n = n.replace("=", ":")
    n = dict([item.split(":") for item in n.split("&")])
    # print(n)
    n = n["page"]
    num = int(n) * 100
    cursor.execute("select * from mtcy order by 评分 ASC limit {},100".format(num))
    # cursor.execute("select * from mtcy  limit {},100".format(num))
    # datas =str(cursor.fetchall())
    datas = """
       <table>
       <tr>
               <th>店名</th>
               <th>评分 </th>
               <th>人均</th>
               <th>地址</th>
               <th>电话</th>
               <th>营业时间段</th>
               <th>店铺详情</th>
             
          </tr>"""
    for data in cursor.fetchall():
        str = """
                               <tr>           
                                 <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td><a href=%s target="_blank">点击查看店铺</a></td>
                                  </tr>

                              """ %data

        datas += str
    cursor.close()
    db.close()
    s = """<div align="center">
         <a  class="next"  href="meituan.py"> 首页</a>
         <a  class="next"  href="meituan.py&page={}"> 下一页</a>
       </div>
       """.format(int(n) + 1)
    datas = datas + s

    with open("static/jj.html", "rb") as file:
        response_body = file.read()
        response_body = re.sub(r"{%content%}", datas + "</table>" + s, response_body.decode('utf-8'))
    return response_body
from urllib.parse import unquote
@route("/xqdj.py")
def xqdj(n):
    n=unquote(n)
    n = n.replace("=", ":")
    n = dict([item.split(":") for item in unquote(n).split("&")])
    print(n["xq"])
    time =datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    print(n["xq"], n["user"], n["address"],n["tel"], n["sex"],n["bz"],time)
    db = pymysql.Connect(host="localhost", port=3306, user="hao", passwd="4786874", db="spider", charset="utf8")
    cursor = db.cursor()

    sql = "INSERT INTO person(小区名字,登记人员,联系电话,家庭住址,性别,备注信息,日期)  VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(n["xq"], n["user"],n["tel"], n["address"],n["sex"],n["bz"],time)
    cursor.execute(sql)
    print("运行到这里了")
    db.commit()

    str = """                   
                                <tr>           
                                <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 </tr>

                             """ % (n["xq"], n["user"],n["tel"], n["address"],n["bz"],n["sex"],time)
    print(str)
    cursor.close()
    db.close()
    s = """<h1> 提交成功</h1>
                 """
    with open("static/xqsj.html", "rb") as file:
        response_body = file.read()
        response_body = re.sub(r"{%content%}", s+str+"</table>", response_body.decode('utf-8'))
    return response_body

@route("/xqsj.py")
def xqdj(n):
    print(n)
    db = pymysql.Connect(host="localhost", port=3306, user="root", passwd="4786874", db="spider", charset="utf8")
    cursor = db.cursor()
    n = n.replace("=", ":")
    n = dict([item.split(":") for item in n.split("&")])
    # print(n)
    n = n["page"]
    num = int(n) * 100
    # cursor.execute("select * from person order by 评分 ASC limit {},100".format(num))
    cursor.execute("select * from person  limit {},100".format(num))
    datas = " "
    for data in cursor.fetchall():
        str = """                   
                              <tr>           
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              </tr>
                          """ % data

        datas += str
    cursor.close()
    db.close()
    s = """<div align="center">
             <a  class="next"  href="xqsj.py"> 首页</a>
             <a  class="next"  href="xqsj.py&page={}"> 下一页</a>
           </div>
           """.format(int(n) + 1)
    datas = datas + s
    with open("static/xqsj.html","rb") as file:
        response_body = file.read()
        response_body = re.sub(r"{%content%}", datas+"</table>"+s, response_body.decode('utf-8'))
    return response_body

@route("/jl.py")
def jl(n):
    n=unquote(n)
    n = n.replace("=", ":")
    n = dict([item.split(":") for item in unquote(n).split("&")])
    print(n)
    if  "dx1" not in n:
        n["dx1"]=0
    if "dx2" not in n:
        n["dx2"] = 0
    if "dx3" not in n:
        n["dx3"] = 0
    if "dx4" not in n:
        n["dx4"] = 0
    if "dx5" not in n:
        n["dx5"] = 0
    time =datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    print(n["fh"],n["dh"],n["bz"], n["dx1"], n["dx2"],n["dx3"], n["dx4"],n["dx5"],time)
    n["hj"]=float(n["dx1"])+ float(n["dx2"])+ float(n["dx3"]) + float(n["dx4"])+ float(n["dx5"])
    print( n["hj"],"8797897")
    db = pymysql.Connect(host="localhost", port=3306, user="hao", passwd="4786874", db="spider", charset="utf8")
    cursor = db.cursor()
    select_count_sql = "SELECT COUNT(1) from jlsj WHERE dh ='{}'".format(n['dh'])
    # 执行查询SQL
    cursor.execute(select_count_sql)
    # 获取查询结果
    count = cursor.fetchone()[0]
    print(count)
    if count == True:
        sql = "delete from jlsj where dh ={}".format(n['dh'])
        cursor.execute(sql)
        db.commit()
    select_count_sql = "SELECT COUNT(1) from jlsj WHERE dh ='{}'".format(n['dh'])
    # 执行查询SQL
    cursor.execute(select_count_sql)
    # 获取查询结果
    count = cursor.fetchone()[0]
    if count == 0:
       sql = "INSERT INTO jlsj(fh,dh,dx1,dx2,dx3,dx4,dx5,hj,time,bz)  VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(n["fh"],n["dh"], n["dx1"], n["dx2"],n["dx3"], n["dx4"],n["dx5"],round(n["hj"],3),time,n["bz"])
    cursor.execute(sql)
    print("运行到这里了")
    db.commit()

    str = """                   
                                <tr>           
                                <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                 <td>%s</td>
                                  <td>%s</td>
                                 <td>%s</td>
                                  <td>%s</td>
                                 </tr>

                             """ % (n["fh"],n["dh"], n["dx1"], n["dx2"],n["dx3"], n["dx4"],n["dx5"],round(n["hj"],3),time,n["bz"])
    print(str)
    cursor.close()
    db.close()
    s = """<h1> 提交成功</h1>
                 """
    with open("static/jlsj.html", "rb") as file:
        response_body = file.read()
        response_body = re.sub(r"{%content%}", s+str+"</table>", response_body.decode('utf-8'))
    return response_body

@route("/jlsj.py")
def jlsj(n):
    print(n)
    db = pymysql.Connect(host="localhost", port=3306, user="root", passwd="4786874", db="spider", charset="utf8")
    cursor = db.cursor()
    n = n.replace("=", ":")
    n = dict([item.split(":") for item in n.split("&")])
    # print(n)
    n = n["page"]
    num = int(n) * 100
    # cursor.execute("select * from person order by 评分 ASC limit {},100".format(num))
    cursor.execute("select * from jlsj  limit {},100".format(num))
    # print(cursor.fetchall())
    datas = " "
    num=0
    for data in cursor.fetchall():
        num+=1
        str1 = """                   
                              <tr>    
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                              <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                               <td>%s</td>
                              </tr>
                          """ %data

        datas += str1
    cursor.execute("select count(1) from jlsj ")
    z=cursor.fetchall()[0][0]
    d=[]
    for i in range(5):
        cursor.execute("select count(1) from jlsj where {} > 0".format("dx"+str(i+1)))
        # print(cursor.fetchall()[0][0])
        d.append(cursor.fetchall()[0][0])
    print(d)
    cursor.execute("select sum(hj) from jlsj ")
    hj=round(cursor.fetchall()[0][0],3)

    # cursor.execute("select count(1) from jlsj where dx1 > 0")
    # d =cursor.fetchall()[0][0]
    # cursor.execute("select count(1) from jlsj where dx2 > 0")
    # d2 = cursor.fetchall()[0][0]
    # print(d,d2)

    str2=""" <tr>         
                          <td>总合计</td>
                          <td>{}</td>
                          <td>{}</td>
                          <td>{}</td>
                          <td>{}</td>
                          <td>{}</td>
                          <td>{}</td>
                          <td>{}</td>
                           <td></td>
                           <td></td>
                          </tr>""".format(z,d[0],d[1],d[2],d[3],d[4],hj)
    datas =datas +str2
    cursor.close()
    db.close()
    s = """<div align="center">
             <a  class="next"  href="jlsj.py"> 首页</a>
             <a  class="next"  href="jlsj.py&page={}"> 下一页</a>
           </div>
           """.format(int(n) + 1)
    datas = datas + s
    with open("static/jlsj.html","rb") as file:
        response_body = file.read()
        response_body = re.sub(r"{%content%}", datas+"</table>"+s, response_body.decode('utf-8'))
    return response_body