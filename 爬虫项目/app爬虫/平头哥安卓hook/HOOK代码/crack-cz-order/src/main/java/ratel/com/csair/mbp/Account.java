package ratel.com.csair.mbp;

import android.content.SharedPreferences;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.inspect.ClassLoadMonitor;
import com.virjar.ratel.api.rposed.RposedHelpers;

import external.com.alibaba.fastjson.JSONObject;

public class Account {
    public static String userName = "";
    public static String password = "";

    private static final String userManagerClassName = "com.csair.mbp.base.d.am";

    public static boolean isLogin() {
        Class<?> userManagerClass = ClassLoadMonitor.tryLoadClass(userManagerClassName);
        return (boolean) RposedHelpers.callStaticMethod(userManagerClass, "c");
    }

    public static String getLoginUserId() {

        if (!isLogin()) {
            return null;
        }

        Class<?> userManagerClass = ClassLoadMonitor.tryLoadClass(userManagerClassName);
        boolean loginTypePsw = (boolean) RposedHelpers.callStaticMethod(userManagerClass, "a");
        if (loginTypePsw) {
            //非会员，应该是第三发登录那种意思???
            return (String) RposedHelpers.callStaticMethod(userManagerClass, "b", "AID");
        } else {
            return (String) RposedHelpers.callStaticMethod(userManagerClass, "b", "CARD_NO");
        }
    }

    public static JSONObject getLoginTempFile() {
        try {
            Class<?> userManagerClass = ClassLoadMonitor.tryLoadClass(userManagerClassName);
            Object a = RposedHelpers.callStaticMethod(userManagerClass, "e", "LoginInfoTempFile");
            //com.csair.mbp.base.d.a
            if (a == null) {
                return null;
            }
            SharedPreferences sharedPreferences = RposedHelpers.getObjectField(a, "a");
            JSONObject jsonObject = new JSONObject();
            for (String key : sharedPreferences.getAll().keySet()) {
                String realKey = (String) RposedHelpers.callMethod(a, "c", key);
                jsonObject.put(realKey, RposedHelpers.callMethod(a, "getString", realKey, "virjar-default"));
            }
            return jsonObject;
        } catch (Throwable throwable) {
            FileLogger.outLog("error", FileLogger.getTrack(throwable));
            return null;
        }
    }
}
