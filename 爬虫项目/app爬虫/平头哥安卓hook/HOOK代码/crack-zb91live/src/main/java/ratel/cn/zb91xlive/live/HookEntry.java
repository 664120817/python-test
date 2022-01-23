package ratel.cn.zb91xlive.live;

import android.app.Dialog;
import android.util.Log;

import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

/**
 * Created by virjar on 2018/10/6.
 */

public class HookEntry implements IRposedHookLoadPackage {
    private static final String tag = "ZB91_HOOK";

    @Override
    public void handleLoadPackage(final RC_LoadPackage.LoadPackageParam lpparam) {
        RposedBridge.hookAllConstructors(Dialog.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(tag, "show dialog", new Throwable());
            }
        });

        crackVIP(lpparam);

        //com.fanwe.hybrid.http.AppRequestCallback#parseActModel
        RposedHelpers.findAndHookMethod("com.fanwe.hybrid.http.AppRequestCallback", lpparam.classLoader,
                "parseActModel", String.class, Class.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "parseActModel: " + param.args[0]);
                        Log.i(tag, "class: " + param.args[1]);
                        Class clazz = (Class) param.args[1];
                        if ("com.fanwe.live.model.App_rechargeActModel".equals(clazz.getName())) {
                            Object rechargeActModel = param.getResult();

                            RposedHelpers.setLongField(rechargeActModel,
                                    "diamonds", 5597);

                        } else if ("com.fanwe.live.model.App_userinfoActModel".equals(clazz.getName())) {
                            Object userinfoActModel = param.getResult();
                            Object user = RposedHelpers.getObjectField(userinfoActModel, "user");

                            RposedHelpers.setLongField(user, "diamonds", 20001);

                        }
                    }
                });

        Log.i(tag, "hook end");
    }


    private void crackVIP(RC_LoadPackage.LoadPackageParam lpparam) {
        //com.fanwe.live.activity.room.LiveLayoutViewerExtendActivity#showScenePayJoinDialog
        RposedHelpers.findAndHookMethod(
                "com.fanwe.live.activity.room.LiveLayoutViewerExtendActivity", lpparam.classLoader,
                "showScenePayJoinDialog",
                int.class, new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        param.setResult(null);
                    }
                }
        );

        //com.fanwe.live.activity.room.LiveLayoutViewerExtendActivity#onScenePayViewerShowCoveringPlayeVideo
        RposedHelpers.findAndHookMethod(
                "com.fanwe.live.activity.room.LiveLayoutViewerExtendActivity", lpparam.classLoader,
                "onScenePayViewerShowCoveringPlayeVideo",
                String.class, int.class, int.class,

                new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);

                        String preview_play_url = (String) param.args[0];
                        int countdown = (int) param.args[1];
                        int is_only_play_voice = (int) param.args[2];
                        Log.i(tag, "preview_play_url: " + preview_play_url + "" +
                                " countdown:" + countdown + " is_only_play_voice:" + is_only_play_voice);

                        param.args[1] = 10000;
                    }
                }
        );
    }
}
