package ratel.crack.yuanrenxue.trip1221;

import android.util.Log;
import android.widget.TextView;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.extension.superappium.sekiro.SekiroStarter;
import com.virjar.ratel.api.inspect.ClassLoadMonitor;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.Constants;
import com.virjar.sekiro.log.SekiroLogger;

import java.lang.reflect.Type;

import external.com.alibaba.fastjson.JSONObject;
import ratel.crack.yuanrenxue.BuildConfig;
import ratel.crack.yuanrenxue.trip1221.pages.IBUHomeActivityPageHandler;
import ratel.crack.yuanrenxue.trip1221.pages.LoginActivityPageHandler;
import ratel.crack.yuanrenxue.trip1221.pages.LoginTypeActivityPageHandler;

public class Trip1221 {
    public static final String tag = "TR_HOOK";

    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {
        SekiroLogger.tag = tag;
        SuperAppium.TAG = tag;
        startUIDriver();
        //RPC.setupRPC();
        startSekiro(lpparam);
        if (BuildConfig.DEBUG) {
            CtripEnglishCrack.handle(lpparam);
        }
        Log.i(tag, "HOOK end!!");
    }

    private static void startSekiro(RC_LoadPackage.LoadPackageParam lpparam) {
        if (lpparam.packageName.equals(lpparam.processName)) {
            SekiroLogger.tag = tag;
            SuperAppium.TAG = tag;
            SekiroStarter.startService("sekiro.virjar.com", Constants.defaultNatServerPort,
                    "virjar-trip");


        }
    }

    private static void startUIDriver() {
        // 启动页和首页
        PageTriggerManager.addHandler("com.ctrip.ibu.myctrip.main.module.home.IBUHomeActivity",
                new IBUHomeActivityPageHandler());

        //登录方式选择页面
        PageTriggerManager.addHandler("com.ctrip.ibu.account.module.login.LoginTypeActivity",
                new LoginTypeActivityPageHandler());

        //登录页面
        PageTriggerManager.addHandler("com.ctrip.ibu.account.module.login.LoginActivity",
                new LoginActivityPageHandler());

//        //登录页面
//        PageTriggerManager.addHandler("com.ctrip.ibu.account.module.login.LoginActivityWithMoreAccount",
//                new LoginActivityWithMoreAccountPageHandler());
    }

    private static void backup(RC_LoadPackage.LoadPackageParam lpparam) {


        //ctrip.android.httpv2.CTHTTPClient#sendRequest
        RposedHelpers.findAndHookMethod(
                "ctrip.android.httpv2.CTHTTPClient", lpparam.classLoader,
                "sendRequest",
                "ctrip.android.httpv2.CTHTTPRequest",
                "ctrip.android.httpv2.CTHTTPCallback",
                new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        String url = "" + RposedHelpers.getObjectField(param.args[0], "a");
                        if (url.contains("json/hotelsearch")) {
                            Log.i(tag, "sendRequest: " + url, new Throwable());
                        }
                    }
                }
        );


        RposedHelpers.findAndHookConstructor(
                "e.h.e.t.e.f", lpparam.classLoader,
                Type.class,
                new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "create e.h.e.t.e.f:  type: " + param.args[0], new Throwable());
                    }
                }
        );


        //ctrip.business.comm.SOTPClient#sendSOTPRequest
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("ctrip.business.comm.SOTPClient", lpparam.classLoader),
                "sendSOTPRequest", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "sendSOTPRequest ", new Throwable());
                    }
                }
        );

        //f.a.l.g#g
        RposedBridge.hookAllConstructors(
                RposedHelpers.findClass("f.a.l.g", lpparam.classLoader),
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "create f.a.l.g: ", new Throwable());
                    }
                }
        );


        //e.h.e.t.e.f#convert
        RposedHelpers.findAndHookMethod("e.h.e.t.e.f", lpparam.classLoader,
                "convert", Object.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "convert input " + JSONObject.toJSONString(param.args[0]));
                        Log.i(tag, "convert output " + JSONObject.toJSONString(param.getResult()));
                        Log.i(tag, "convert output type: " + param.getResult().getClass());
                    }
                });


        //com.ctrip.ibu.hotel.business.response.java.hotellst.HotelBaseInfoType
        RposedBridge.hookAllConstructors(
                RposedHelpers.findClass("com.ctrip.ibu.hotel.business.response.java.hotellst.HotelBaseInfoType", lpparam.classLoader),
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "create HotelBaseInfoType " + param.thisObject, new Throwable());
                    }
                }
        );

        //private void setText(CharSequence text, BufferType type,
        //                         boolean notifyBefore, int oldlen) {}
        RposedHelpers.findAndHookMethod(TextView.class, "setText", CharSequence.class, TextView.BufferType.class, boolean.class, int.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        String textContent = param.args[0] + "";
                        if (textContent.contains("石酒店")) {
                            Log.i(tag, "setText for textView:" + textContent);
                            Log.i(tag, "hint content:" + textContent, new Throwable());
                        }
                    }
                });
        //e.h.e.l.c.b.g
        final Class<?> aClass = RposedHelpers.findClass("e.h.e.l.c.b.g", lpparam.classLoader);
        ClassLoadMonitor.addClassLoadMonitor(new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {
                if (!aClass.isAssignableFrom(clazz)) {
                    return;
                }
                //
                RposedHelpers.findAndHookMethod(clazz, "getHotelName", new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "getHotelName :" + param.getResult() + " method: " + param.thisObject.getClass().getName());
                    }
                });
            }
        });

    }

}
