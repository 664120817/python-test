package ratel.com.csair.mbp;

import android.app.Activity;
import android.os.Handler;
import android.os.Looper;
import android.text.TextUtils;
import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.inspect.ClassLoadMonitor;
import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.Constants;
import com.virjar.sekiro.api.SekiroClient;
import com.virjar.sekiro.log.SekiroLogger;

import java.io.File;
import java.util.List;
import java.util.Random;
import java.util.Set;

import ratel.com.csair.mbp.page.AuthorityApplyActivityPageHandler;
import ratel.com.csair.mbp.page.CSMBPActivityPageHandler;
import ratel.com.csair.mbp.page.LoginActivityPageHandler;
import ratel.com.csair.mbp.page.PrivacyActivityPageHandler;
import ratel.com.csair.mbp.page.UpdateActivityPageHandler;
import ratel.com.csair.mbp.page.WelcomeActivityPageHandler;
import ratel.com.csair.mbp.sekiro.CreateOrderAction;
import ratel.com.csair.mbp.sekiro.DecodeAction;
import ratel.com.csair.mbp.sekiro.EncodeAction;
import ratel.com.csair.mbp.sekiro.ExecuteCmdAction;
import ratel.com.csair.mbp.sekiro.LogViewAction;
import ratel.com.csair.mbp.sekiro.MUserInfoAction;
import ratel.com.csair.mbp.sekiro.PostAction;
import ratel.com.csair.mbp.sekiro.WTokenAction;
import ratel.com.csair.mbp.services.ConfigManager;
import ratel.com.csair.mbp.services.DroidSword;
import ratel.com.csair.mbp.services.OrderServices;
import ratel.com.csair.mbp.services.PermissionMonitorHook;
import ratel.com.csair.mbp.utils.OrderLogger;

/**
 * Created by virjar on 2018/10/6.
 */

public class HookEntry implements IRposedHookLoadPackage {
    public static final String TAG = "CZ_HOOK";

    private static SekiroClient sekiroClient = null;


    @Override
    public void handleLoadPackage(final RC_LoadPackage.LoadPackageParam lpparam) {

        // https://m.csair.com/CSMBP.apk 客户端下载地址(当前插件只能适配南航 3.x.x)

        // 1. 适配到 4.x.x
        // 2. 实现生单流程
        // apk 下载地址: http://oss.virjar.com/ratel/com.csair.mbp_3.9.6_20200716_orinal.apk

        FileLogger.startRecord(new File(RatelToolKit.whiteSdcardDirPath, "fileLog"));


        RposedHelpers.findAndHookMethod(Activity.class, "onResume", new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                FileLogger.outLog(TAG, "top activity:" + param.thisObject.getClass());
            }
        });

        PermissionMonitorHook.denyAllPermission();

        DroidSword.startDroidSword();

        if (RatelToolKit.processName.equals(RatelToolKit.packageName)) {
            switchEvnIfNeed();

            OrderLogger.startRecord();
            SekiroLogger.tag = TAG;
            SuperAppium.TAG = TAG;

            new PostAction();


            RposedHelpers.findAndHookMethod(Activity.class, "onResume", new RC_MethodHook() {
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    if (!param.thisObject.getClass().getName().contains("com.csair.mbp.CSMBPActivity")) {
                        return;
                    }
                    if (sekiroClient != null) {
                        return;
                    }
                    new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            String clientId = Account.getLoginUserId();
                            if (TextUtils.isEmpty(clientId)) {
                                return;
                            }
                            String deviceClientId = ConfigManager.getInstance().getSetting().clientId;
                            if (deviceClientId == null) {
                                deviceClientId = "";
                            }
                            deviceClientId = deviceClientId.replaceAll(" ", "").trim();
                            clientId = clientId + "_" + deviceClientId;
                            sekiroClient = SekiroClient.start("sekiro.virjar.com", Constants.defaultNatServerPort, clientId
                                    , "cz_booking_slave_order")

                                    .registerHandler(new DecodeAction())
                                    .registerHandler(new EncodeAction())
                                    .registerHandler(new WTokenAction())

                                    .registerHandler(new PostAction())

                                    .registerHandler(new MUserInfoAction())
                                    .registerHandler(new CreateOrderAction())
                                    .registerHandler(new LogViewAction())
                                    .registerHandler(new ExecuteCmdAction())

                            ;
                        }
                    }, 1000);

                }
            });

            OrderServices.start();


        }


        //com.csair.mbp.source.status.d.c#request
        //com.csair.mbp.book.international.e.a#request
        ClassLoadMonitor.addClassLoadMonitor("com.csair.mbp.book.international.e.a", new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {
                FileLogger.outLog("find class: " + clazz.getName());
                RposedHelpers.findAndHookMethod(clazz, "request", new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        FileLogger.outLog("request body: " + param.getResult());
                        FileLogger.outTrack("com.csair.mbp.book.international.e.a#request");
                    }
                });

                // public java.lang.Object response(org.json.JSONObject jSONObject) {
                RposedHelpers.findAndHookMethod(clazz, "response", "org.json.JSONObject", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        FileLogger.outLog("response body: " + param.args[0]);
                        FileLogger.outTrack("com.csair.mbp.book.international.e.a#response");
                    }
                });
            }


        });


        //com.csair.mbp.netrequest.net.okhttp.d#a(java.lang.String, java.lang.String, int, com.csair.mbp.netrequest.net.okhttp.b.b)
        ClassLoadMonitor.findAndHookMethod("com.csair.mbp.netrequest.net.okhttp.d", "a",
                String.class, String.class, int.class, "com.csair.mbp.netrequest.net.okhttp.b.b", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        FileLogger.outLog("begin of request-> \n url: " + param.args[0]
                                + "\n  body: " + param.args[1]
                                + "\n  timeout: " + param.args[2]
                                + "\n  handler:" + param.args[3].getClass().getName());
                    }
                });

        setupUIDriver();


        if (BuildConfig.DEBUG) {
            Debug.entry(lpparam);
        }
        Log.i(TAG, "hook end");
    }


    private void switchEvnIfNeed() {
        Random random = new Random();
        List<ConfigManager.Account> accountList = ConfigManager.getInstance().getAccountList();
        Set<String> strings = RatelToolKit.virtualEnv.availableUserSet();
        if (accountList.isEmpty()) {

            String nowDevices = "no_login_" + random.nextInt(10000);
            for (String str : strings) {
                if (str.startsWith("no_login_")) {
                    RatelToolKit.virtualEnv.removeUser(str);
                }
            }
            RatelToolKit.virtualEnv.switchEnv(nowDevices);
        } else {
            int index = random.nextInt(accountList.size());
            ConfigManager.Account account = accountList.get(index);
            String deviceEnd = "_vd_" + ConfigManager.getInstance().getSetting().multiDevice + "_vd";
            RatelToolKit.virtualEnv.switchEnv("login_" + account.account + deviceEnd);
            Account.userName = account.account;
            Account.password = account.password;

            for (String str : strings) {
                if (str.startsWith("login_")
                        && !str.endsWith(deviceEnd)) {
                    RatelToolKit.virtualEnv.removeUser(str);
                }
            }
        }
    }

    private void setupUIDriver() {
        PageTriggerManager.addHandler("com.csair.mbp.main.home.PrivacyActivity", new PrivacyActivityPageHandler());
        PageTriggerManager.addHandler("com.csair.mbp.main.home.AuthorityApplyActivity", new AuthorityApplyActivityPageHandler());
        PageTriggerManager.addHandler("com.csair.mbp.CSMBPActivity", new CSMBPActivityPageHandler());
        PageTriggerManager.addHandler("com.csair.mbp.login.activity.LoginActivity", new LoginActivityPageHandler());
        PageTriggerManager.addHandler("com.csair.mbp.launcher.WelcomeActivity", new WelcomeActivityPageHandler());
        PageTriggerManager.addHandler("com.csair.mbp.book.update.UpdateActivity", new UpdateActivityPageHandler());
    }

}
