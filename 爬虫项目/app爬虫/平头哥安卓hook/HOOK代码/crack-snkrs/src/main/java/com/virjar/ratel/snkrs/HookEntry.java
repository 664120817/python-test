package com.virjar.ratel.snkrs;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.socketmonitor.SocketMonitor;
import com.virjar.ratel.api.extension.socketmonitor.observer.FileLogEventObserver;
import com.virjar.ratel.api.extension.superappium.sekiro.SekiroStarter;
import com.virjar.ratel.api.inspect.ClassLoadMonitor;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.Constants;

import java.io.File;
import java.util.HashMap;

import external.com.alibaba.fastjson.JSON;


public class HookEntry implements IRposedHookLoadPackage {
    public static final String TAG = "SuperAppium";
    private static AlertDialog alertDialog = null;

    // private static boolean hasHookWindowManager = false;

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) {
        if (!lpparam.packageName.equals(lpparam.processName)) {
            return;
        }
        Log.i(TAG, "handleLoadPackage");

        ClassLoadMonitor.addClassLoadMonitor("com.nike.snkrs.core.idnaccount.user.network.IdnUserFetchRequestKey", new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {
                Log.i(TAG, "load IdnUserFetchRequestKey class", new Throwable());
            }
        });

        //启动dump服务器
        SekiroStarter.startService("sekiro.virjar.com", Constants.defaultNatServerPort);

        SocketMonitor.setPacketEventObserver(new FileLogEventObserver(new File(RatelToolKit.whiteSdcardDirPath, "socketMonitor")));


        RposedBridge.hookAllConstructors(
                RposedHelpers.findClass("com.nike.snkrs.core.idnaccount.user.models.IdnUserModel", lpparam.classLoader),
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "create IdnUserModel: " + JSON.toJSONString(ForceFiledViewer.toView(param.thisObject)), new Throwable());
                    }
                }
        );

        //com.nike.snkrs.core.idnaccount.user.network.IdnUserFetchRequestKey#IdnUserFetchRequestKey
        RposedBridge.hookAllConstructors(RposedHelpers.findClass("com.nike.snkrs.core.idnaccount.user.network.IdnUserFetchRequestKey", lpparam.classLoader),
                new RC_MethodHook() {
                    @Override

                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "constructor of IdnUserFetchRequestKey: " + JSON.toJSONString(ForceFiledViewer.toView(param.args)), new Throwable());
                    }
                });
        //com.nike.snkrs.core.idnaccount.user.network.IdnUserFetcher#fetch
        RposedHelpers.findAndHookMethod("com.nike.snkrs.core.idnaccount.user.network.IdnUserFetcher", lpparam.classLoader,
                "fetch", "com.nike.snkrs.core.idnaccount.user.network.IdnUserRequestKey", new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "fetch idn user, request: " + JSON.toJSONString(ForceFiledViewer.toView(param.args[0])), new Throwable());
                        Log.i(TAG, "IdnUserRequestKey class: " + param.args[0].getClass());
                    }
                });

        //com.nike.snkrs.core.idnaccount.user.IdnUserService$storeKey$1#apply
        RposedHelpers.findAndHookMethod("com.nike.snkrs.core.idnaccount.user.IdnUserService$storeKey$1", lpparam.classLoader,
                "apply", String.class, new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "IdnUserService$storeKey$1#apply :" + param.args[0], new Throwable());
                    }
                });


        Log.i(TAG, "hook end");
    }

    static {
        ForceFiledViewer.addForceViewConfig("android.content.pm.ApplicationInfo");
    }

    private static void backup(RC_LoadPackage.LoadPackageParam lpparam) {


        //com.nike.snkrs.core.idnaccount.user.IdnUserRefreshListener.updateIdnUserPrefs
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("com.nike.snkrs.core.idnaccount.user.IdnUserRefreshListener", lpparam.classLoader)
                , "updateIdnUserPrefs", new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "updateIdnUserPrefs: " + JSON.toJSONString(ForceFiledViewer.toView(param.args[0])));
                    }
                }
        );


        //expires=1575700191&device_name=MI+9+Transparent+Edition&method=token&device_id=E81809057639AE4E800CC109317FC671&apikey=I6FWDlFGVAcR2YrGZaG1cBNtZmbwL33t&v=1&device_type=3&vcode=c6103c95c880850f07c8028d3ad1cb4d&timestamp=1575613791&info=%7B%22api_level%22%3A28%2C%22screen_height%22%3A2135%2C%22screen_width%22%3A1080%2C%22model%22%3A%22MI+9+Transparent+Edition%22%2C%22isroot%22%3A0%2C%22is_baidu_app%22%3A0%2C%22push_sdk_version%22%3A62%2C%22manufacturer%22%3A%22Xiaomi%22%7D

        RposedHelpers.findAndHookMethod(HashMap.class, "put", Object.class, Object.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                if (!(param.args[0] instanceof CharSequence)) {
                    return;
                }
                String key = param.args[0].toString();
                if ("firstName".equals(key) || "lastName".equals(key)) {
                    Log.i(TAG, "set value to hashMap key: " + key + " value: " + param.args[1]);
                    Log.i(TAG, "stack: ", new Throwable());
                }

            }
        });

        //android.app.Activity.onActivityResult(int requestCode, int resultCode, Intent data)
        RposedHelpers.findAndHookMethod(Activity.class,
                "onActivityResult",
                int.class, int.class, Intent.class,
                new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "onActivityResult for activity: " + param.thisObject.getClass().getName() + " requestCode:" + param.args[0]
                                + " resultCode:" + param.args[1] + " data:"
                                + JSON.toJSONString(ForceFiledViewer.toView(param.args[2])));
                    }
                }
        );


        RposedHelpers.findAndHookMethod(Activity.class, "onResume", new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(TAG, "activity: " + param.thisObject.getClass().getName() + "  onResume");
            }
        });


    }

}
