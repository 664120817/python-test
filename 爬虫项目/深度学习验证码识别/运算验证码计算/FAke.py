from flask import Flask,render_template,request
app = Flask(__name__)
@app.route('/')
def welcome(name='gfgf' ,ooo = 'girl'): #参数允许有默认值ooo =girl
    print(name,ooo)
    return 'Hello World,%s,%s'%(name,ooo)
    image


if __name__ == '__main__':
    app.run(debug=True,port=88,host='127.0.0.1')