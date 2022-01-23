package ratel.crack.yuanrenxue.trip1221;

import android.util.Log;
import android.widget.TextView;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RC_MethodReplacement;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

import java.io.File;
import java.net.URL;
import java.util.Map;

import external.com.alibaba.fastjson.JSON;
import external.com.alibaba.fastjson.JSONObject;
import external.org.apache.commons.lang3.StringUtils;

public class CtripEnglishCrack {
    public static final String tag = Trip1221.tag;


    public static void handle(RC_LoadPackage.LoadPackageParam lpparam) {
        Log.i(tag, "hook processor" + CtripEnglishCrack.class.getName());

        RposedBridge.hookAllConstructors(URL.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(tag, "access url " + param.thisObject);
            }
        });

        // private void setText(CharSequence text, BufferType type,
        //                         boolean notifyBefore, int oldlen) {
        RposedHelpers.findAndHookMethod(TextView.class,
                "setText",
                CharSequence.class, TextView.BufferType.class, boolean.class, int.class
                , new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        TextView textView = (TextView) param.thisObject;
                        //textView.setText();
//斯坦福酒店
                        String text = param.args[0].toString();
                        if (StringUtils.contains(text, "CNY240")) {
                            Log.i(tag, "setup key: " + text, new Throwable());
                        }
                    }
                });
//

        //e.h.e.k.d.c.h#a(e.h.e.l.c.b.g, boolean, android.widget.TextView, android.widget.TextView, boolean, java.util.List<java.lang.String>)
        Class<?> hClass = RposedHelpers.findClass("e.h.e.k.d.c.h", lpparam.classLoader);
        RposedHelpers.findAndHookMethod(hClass, "a",
                "e.h.e.l.c.b.g", boolean.class, TextView.class, TextView.class,
                boolean.class, java.util.List.class, new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "aaa : hClass " + param.args[0].getClass().getName() + " data: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[0])));
                    }
                });


        FileLogger.startRecord(new File(RatelToolKit.whiteSdcardDirPath, "logs"));
        //ctrip.android.httpv2.CTHTTPClient#sendRequest
        RposedHelpers.findAndHookMethod(
                RposedHelpers.findClass("ctrip.android.httpv2.CTHTTPClient", lpparam.classLoader),
                "sendRequest",
                "ctrip.android.httpv2.CTHTTPRequest", "ctrip.android.httpv2.CTHTTPCallback",
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "sendRequest: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[0])));
                        FileLogger.outLog("sendRequest: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[0], false)));
                    }
                }
        );


        //ctrip.android.httpv2.CTHTTPRequest#buildHTTPRequest
        RposedHelpers.findAndHookMethod(
                RposedHelpers.findClass("ctrip.android.httpv2.CTHTTPRequest", lpparam.classLoader),
                "buildHTTPRequest",
                String.class, Object.class, Class.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        FileLogger.outLog("buildHTTPRequest -> path: " + param.args[0] + "  param: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[1])) + " class: " + param.args[2]);
                    }
                }
        );


        //e.h.e.t.b.a#a
        RposedHelpers.findAndHookConstructor(
                RposedHelpers.findClass("e.h.e.t.b.a", lpparam.classLoader),
                String.class, String.class, Object.class, Class.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        FileLogger.outLog("buildHTTPRequestNew -> n:" + param.args[0] + " path: " + param.args[1] + "  param: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[2])) + " class: " + param.args[3]);
                    }
                }
        );

        //com.ctrip.ibu.hotel.business.request.java.HotelSearchJavaRequest#setSearchSort
        RposedHelpers.findAndHookMethod(
                RposedHelpers.findClass("com.ctrip.ibu.hotel.business.request.java.HotelSearchJavaRequest", lpparam.classLoader),
                "setSearchSort",
                "com.ctrip.ibu.hotel.business.model.EHotelSort", new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "setSearchSort : " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[0])));
                    }
                }
        );


        //ctrip.android.httpv2.CTHTTPClientExecutor#a(ctrip.android.httpv2.CTHTTPClient.RequestDetail, java.util.Map<java.lang.String,java.lang.String>, boolean, int, java.lang.String, byte[])
//        if (lpparam.packageName.equals(lpparam.processName)) {
//            SekiroStarter.startService("sekiro.virjar.com", Constants.defaultNatServerPort,
//                    "virjar");
//
//            SekiroStarter.getDefaultSekiroClient().registerHandler(new CtripEnglishHotelSearch());
//        }

        ForceFiledViewer.addSkipViewConfig("org.joda.time");
        //e.h.e.l.g.r.c.b.b#b(org.joda.time.DateTime, org.joda.time.DateTime, com.ctrip.ibu.hotel.business.model.IHotel, com.ctrip.ibu.hotel.module.filter.HotelFilterParams, java.lang.String, java.lang.String, java.lang.String, android.content.Intent)
        RposedBridge.hookAllConstructors(
                RposedHelpers.findClass("e.h.e.l.g.r.c.b.b", RatelToolKit.hostClassLoader),
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "create filterParams obj:" + param.args[4] + " " + param.args[5] + " " + param.args[6], new Throwable());
                    }
                }
        );
        openLogger("CLOG");
        Log.i(tag, "hook end");
    }

    private static void openLogger(final String tag) {
        //ctrip.foundation.util.LogUtil#d(java.lang.String)
        Class<?> logUtilClass = RposedHelpers.findClass("ctrip.foundation.util.LogUtil", RatelToolKit.hostClassLoader);
        RposedHelpers.findAndHookMethod(logUtilClass, "d", String.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(tag, "d:" + param.args[0]);
                String message = param.args[0].toString();
                if (message.contains("PRequest->error:9000")) {
                    Log.i(tag, "the login error response", new Throwable());
                }
            }
        });
        RposedHelpers.findAndHookMethod(logUtilClass, "v", String.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(tag, "v:" + param.args[0]);
            }
        });
        RposedHelpers.findAndHookMethod(logUtilClass, "e", String.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(tag, "e:" + param.args[0]);
            }
        });

        //ctrip.foundation.util.LogUtil#xlgEnabled
        RposedHelpers.findAndHookMethod(logUtilClass, "xlgEnabled", new RC_MethodReplacement() {
            @Override
            protected Object replaceHookedMethod(MethodHookParam param) throws Throwable {
                return true;
            }
        });


        //ctrip.foundation.util.UBTLogPrivateUtil#logMonitor
        Class<?> UBTLogPrivateUtilClass = RposedHelpers.findClass("ctrip.foundation.util.UBTLogPrivateUtil", RatelToolKit.hostClassLoader);
        RposedHelpers.findAndHookMethod(UBTLogPrivateUtilClass, "logMonitor",
                String.class, Number.class, Map.class, new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "logMonitor: " + param.args[0] + " " + param.args[1]);
                        Log.i(tag, "logMonitor: " + JSON.toJSONString(param.args[2]));
                    }
                }
        );

    }
}
