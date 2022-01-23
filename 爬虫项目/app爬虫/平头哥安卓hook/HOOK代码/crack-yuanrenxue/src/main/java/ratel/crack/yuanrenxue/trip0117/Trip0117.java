package ratel.crack.yuanrenxue.trip0117;

import android.util.Log;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.extension.superappium.sekiro.SekiroStarter;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.Constants;
import com.virjar.sekiro.log.SekiroLogger;

import ratel.crack.yuanrenxue.BuildConfig;
import ratel.crack.yuanrenxue.trip0117.page.IBUHomeActivityPageHandler;
import ratel.crack.yuanrenxue.trip0117.page.LoginTypeActivityPageHandler;
import ratel.crack.yuanrenxue.trip1221.pages.LoginActivityPageHandler;

public class Trip0117 {
    public static final String tag = "TR_HOOK";

    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {
        SekiroLogger.tag = tag;
        SuperAppium.TAG = tag;
        if (lpparam.processName.equals(lpparam.packageName)) {
            setupUI();
        }

        Log.i(tag, "HOOK end!!");
    }

    private static void setupUI() {

        if (BuildConfig.DEBUG) {
            SekiroStarter.startService(
                    "sekiro.virjar.com", Constants.defaultNatServerPort,
                    "trip-0117"
            );
        }

        PageTriggerManager.addHandler("com.ctrip.ibu.myctrip.main.module.home.IBUHomeActivity",
                new IBUHomeActivityPageHandler());

        //com.ctrip.ibu.account.module.login.LoginTypeActivity
        PageTriggerManager.addHandler("com.ctrip.ibu.account.module.login.LoginTypeActivity",
                new LoginTypeActivityPageHandler());

        //登录页面
        PageTriggerManager.addHandler("com.ctrip.ibu.account.module.login.LoginActivity",
                new LoginActivityPageHandler());

    }
}
