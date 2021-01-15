import frida,sys,os,time

def adbforward():
    os.system("adb forward tcp:27043 tcp:27043")
    os.system("adb forward tcp:27042 tcp:27042")

hook_getUserInfo = """

 Java.perform(
     function(){
     var UserInfo = Java.use('com.ss.android.common.applog.UserInfo');
     UserInfo.getUserInfo.overload('int', 'java.lang.String', '[Ljava.lang.String;', 'java.lang.String').implementation = function(v1,v2,v3,v4){
     send(v1);
     send(v2);
     send(v3);
     send(v4);
     var usr = this.getUserInfo(v1,v2,v3,v4);
     send(user);
     return usr;
     }
     }
     );

"""

hook_code="""
rpc.exports = {
 
 get_sing: function(timstamp,url,userinfo_array,device_id){
 var sig = "";
 Java.perfrom(
 function(){
 var UserInfo = Java.use('com.ss.android.common.applog.UserInfo');
 var EagleEye = Java.use('com.ss.android.common.applog.EagleEye');
 var StcSDKFactory = Java.use('com.ss.sys.ces.out.StcSDKFactory');
  var GlobalContext = Java.use('com.ss.android.common.applog.GlobalContext');
 var AwemeApplication = Java.use('com.ss.android.ugc.aweme.app.AwemeApplication');
 var sdk = StcSDKFactory.getSDK(GlobalContext.getContext(),AwemeApplication.p().m());
 
 var userinfo = UserInfo.getUserInfo('timstamp,url,userinfo_array,device_id');
 var as = userinfo.substring(0,22);
 var cp =userinfo.substring(22,userinfo.length);
 var mas = EagleEye.byteArrayToHexStr(sdk.encode(substring.getBytes(as)))
 sig ='&as='+as+'&cp=+cp+'&mas='+mas;
 
 
 }
 )
 return sig
 }
 };
 function getBytes(s){
 var bytes=[];
     for (var i=0;i<s.length;i++){
     bytes.push(s.charCodeAt(i));
     return bytes
     }
 
 
 
 }
"""
def get_sing_hook(script):
    timestamp_w = time.time()
    timestamp = int(timestamp_w)
    device_id ="835268664374951"
    userinfo = ['sdk_version', '1.3.0', 'ts', str(timestamp), 'app_type', 'lite', 'os_api', '23', 'device_type', 'Nexus 6P',
            'device_platform', 'android', 'ssmix', 'a', 'iid', '91658564592', 'manifest_version_code', '203', 'dpi',
            '560',
            'version_code', '203', 'app_name', 'douyin_lite', 'version_name', '2.0.3', 'openudid', 'dd08f504420bcde0',
            'device_id', str(device_id), 'resolution', '1440*2392', 'os_version', '6.0', 'language', 'zh',
            'device_brand', 'google',
            'ac', 'wifi', 'update_version_code', '2030', 'aid', '2329', 'channel', 'xiaomi', '_rticket',
            str(timestamp_w),
            'dwinfo',
            '5r_u5O7C8fL-_On08vO_p_Po8fGxv_zw_O3C8fL-_On08vO_p_Po8fGxv__87vjC7un86fTy87-n5r_-6O_v-PPpv6fmv-nk7fi_p62xv_D-_r-nrbG_8PP-v6etsb_5__C_p62xv_H8_r-nrbG__vjx8dT5v6etsb_-9Pm_p62xv-3u_r-nrbG_7-7u9L-nrbG___T5v6etsb_x_Om_p62xv_Hy8_r0v6etsb_z9Pm_p62xv-70-b-nrbG__-q_p62xv_70v6etsb_4_O_7_vO_p62xv-3-9L-nrbG_6fz-v6et4LG_8_j0-vX_8u_08_q_p8bA4LG_6vT79ML08_vyv6fG5r_q9Pv0wvP88Pi_p7_39Pzz-uf1_PP6v7G_6vT79MLw_P6_p7-t_qelr6erpaevpKeoqKeopb-xv-_u7vS_p7CopLG_9O7C_ujv7_jz6b-nrODAsb_--PHxv6fGwLG_8fL-_On08vPC8PL5-L-nrbG_8fL-_On08vPC7vjp6fTz-r-nrbG_7uj_8PTpwun08Pi_p6yoqq6pq6iupamlqK2xv73x_PP66Pz6-L-nv-f1sN7Tv7G_7fL07r-n8-jx8eA=']

    # infos1 = "sdk_version,1.3.0"
    url = 'https://iu.snssdk.com/location/locate/?sdk_version=1.3.0&ts={}&app_type=lite&os_api=23&device_type=Nexus 6P&device_platform=android&ssmix=a&iid=91658564592&manifest_version_code=203&dpi=560&version_code=203&app_name=douyin_lite&version_name=2.0.3&openudid=dd08f504420bcde0&device_id=69852570923&resolution=1440*2392&os_version=6.0&language=zh&device_brand=google&ac=wifi&update_version_code=2030&aid=2329&channel=xiaomi&_rticket={}'.format(timestamp, timestamp_w)

    # print(','.join(infos))
    sig = script.exports.getsig(timestamp, url, userinfo , str(device_id))
    print('sig:', sig)
    return sig
def on_message(message, data):
    if message['type'] == 'send':
        print("[*]{0}".format(message['payload']))

    else:
        print(message)


#
def get_sing(script ,timstamp,url,userinfo,device_id):
    return  script.getsing(timstamp,url,userinfo,str(device_id))

process = frida.get_remote_device().attach('com.ss.android.ugc.aweme.lite')  # 获取包名
script = process.create_script(hook_code)  # 获取类
script.on('message', on_message)
print('[*] Running CTF')
script.load()
# get_sing_hook(script)
sys.stdin.read()