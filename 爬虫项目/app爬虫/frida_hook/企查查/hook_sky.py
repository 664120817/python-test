import frida,sys

#Android 11.4.0
hook_code = '''
rpc.exports = {
    getsig: function(url, app_version){
        var sig = {"tyc-hi":"", "Authorization":"", "duid":"", "deviceID":""};
        Java.perform(
            function(){
                var dp = Java.use('com.tianyancha.skyeye.utils.dp');
                var duid = dp.g();
                var authorization = dp.I();
                var device_id = dp.i()
                var tyc = dp.a(url, authorization, app_version, '', device_id, "slat")

                sig["tyc-hi"] = tyc;
                sig["Authorization"] = authorization;
                sig["duid"] = duid;
                sig["deviceID"] = device_id;
            }
        )
        return sig;
    }
}
'''


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

def hook_prepare():
    process = frida.get_usb_device().attach('com.tianyancha.skyeye')
    script = process.create_script(hook_code)
    script.on('message', on_message)
    script.load()
    return script

#sig = script.exports.getsig("https://api4.tianyancha.com/services/v3/t/common/baseinfoV5/150041670","Android 11.4.0")
#print(sig)
#sys.stdin.read()