package ratel.crack.yuanrenxue;

import android.content.Intent;
import android.os.Parcel;
import android.util.Log;
import android.widget.TextView;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.socketmonitor.SocketMonitor;
import com.virjar.ratel.api.extension.socketmonitor.observer.FileLogEventObserver;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

import java.io.File;
import java.net.URL;
import java.util.HashMap;

import external.com.alibaba.fastjson.JSONObject;

public class TripHookEntry {
    public static String TAG = "TR_HOOK";

    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {


        //private void setText(CharSequence text, BufferType type,
        //                         boolean notifyBefore, int oldlen) {}
        RposedHelpers.findAndHookMethod(TextView.class, "setText", CharSequence.class, TextView.BufferType.class, boolean.class, int.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        String textContent = param.args[0] + "";
                        Log.i(TAG, "setText for textView:" + textContent);
                        if (textContent.contains("格林豪泰酒店")) {
                            Log.i(TAG, "hint content:" + textContent, new Throwable());
                        }
                    }
                });

        SocketMonitor.setPacketEventObserver(new FileLogEventObserver(
                new File(RatelToolKit.whiteSdcardDirPath, "socketMonitor")
        ));

        RposedHelpers.findAndHookMethod(HashMap.class, "put", Object.class, Object.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                super.afterHookedMethod(param);
                Log.i(TAG, "put: " + param.args[0] + " value:" + param.args[1]);
            }
        });
    }


    private static void backup() {

        // pojo hook
        //com.ctrip.ibu.hotel.business.response.java.hotellst.HotelInfo
        RposedBridge.hookAllConstructors(
                RposedHelpers.findClass("com.ctrip.ibu.hotel.business.response.java.hotellst.HotelInfo", RatelToolKit.hostClassLoader),
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "new HotelInfo:" + JSONObject.toJSONString(ForceFiledViewer.toView(this)));
                        Log.i(TAG, "stack trace:", new Throwable());
                    }
                }
        );

        //ctrip.business.comm.SOTPClient$WrapSOTPCallback.invokeCallback
        RposedHelpers.findAndHookMethod(
                RposedHelpers.findClass("ctrip.business.comm.SOTPClient$WrapSOTPCallback", RatelToolKit.hostClassLoader),
                "invokeCallback",
                "ctrip.business.comm.Task", "ctrip.business.BusinessResponseEntity", "ctrip.business.BusinessRequestEntity",
                new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Object request = param.args[2];
                        Object response = param.args[1];

                        Log.i(TAG, "request: " + JSONObject.toJSONString(ForceFiledViewer.toView(
                                RposedHelpers.callMethod(request, "getRequestBean")
                        )));

                        Log.i(TAG, "response: " + JSONObject.toJSONString(ForceFiledViewer.toView(
                                RposedHelpers.callMethod(response, "getResponseBean")
                        )));
                    }
                }
        );


        // hook url构造函数
        RposedBridge.hookAllConstructors(URL.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                String url = param.thisObject + "";
                Log.i(TAG, "access url:" + url);
                if (url.contains("thekey")) {
                    Log.i(TAG, "hint url:", new Throwable());
                }
            }
        });

        //intent hook
//        Intent intent = new Intent(RatelToolKit.sContext, MainActivity.class);
//        intent.putExtra("hotelId", "13333");
//
//        RatelToolKit.sContext.startActivity(new Intent(RatelToolKit.sContext, MainActivity.class));

        RposedHelpers.findAndHookMethod(Intent.class, "writeToParcel", Parcel.class, int.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Intent intent = (Intent) param.thisObject;
                        intent.getStringExtra("test");
                        String sss = JSONObject.toJSONString(ForceFiledViewer.toView(intent));
                        loge("Result", sss);
                        Log.i(TAG, "intent writeToParcel: " + sss);
                        Log.i(TAG, "intent writeToParcel trace:", new Throwable());
                    }
                });
    }


    public static void loge(String tag, String msg) {
        if (tag == null || tag.length() == 0 || msg == null || msg.length() == 0) {
            return;
        }
        int segmentSize = 3 * 1024;
        long length = msg.length();
        if (length <= segmentSize) {// 长度小于等于限制直接打印
            Log.e(tag, msg);
        } else {
            while (msg.length() > segmentSize) {// 循环分段打印日志
                String logContent = msg.substring(0, segmentSize);
                msg = msg.replace(logContent, "");
                Log.i(tag, logContent);
            }
            Log.i(tag, msg);// 打印剩余日志
        }

    }

}
