from flask import Flask, request
import hook_sky

script_exports_rpc = None
app = Flask(__name__)

@app.route('/hello')
def print_hello():
    return 'hello'

@app.route("/getsigs")
def getsigs():
    try:
        req_url = request.args.get('url')
        print(req_url)
        app_version = request.args.get('version')
        print(app_version)
    except Exception as e:
        print(e)
        return "异常情况"
    else:
        return script_exports_rpc.getsig(req_url, app_version)

if __name__ == '__main__':
    print('start')
    #global script_exports_rpc

    #开启Hook 把Hook程序注入设备
    script_exports = hook_sky.hook_prepare()

    script_exports_rpc = script_exports
    print(script_exports_rpc)

    #运行flask 监听5001端口
    app.run(host='0.0.0.0', port=5001)
