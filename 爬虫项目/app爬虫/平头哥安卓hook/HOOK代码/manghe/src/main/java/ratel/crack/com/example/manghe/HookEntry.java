package ratel.crack.com.example.manghe;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.LayoutInflater;
import android.widget.FrameLayout;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

/**
 * Created by virjar on 2018/10/6.
 */

public class HookEntry implements IRposedHookLoadPackage {
    private static final String tag = "DEMO_HOOK";


//    @Override
//    public void handleLoadPackage(final RC_LoadPackage.LoadPackageParam lpparam) {
//
//        addFloatingButtonForActivity(lpparam);
//        Log.i(tag, "hook end");
//    }


    @Override
    public void handleLoadPackage(final RC_LoadPackage.LoadPackageParam lpparam) throws Throwable{

        addFloatingButtonForActivity(lpparam);
        Log.i(tag, "hook start");
        if (lpparam.packageName.equals("com.example.manghe")) {
            Class<?>  MysteryBoxclass = lpparam.classLoader.loadClass("com.example.manghe.MysteryBox");
            RposedHelpers.findAndHookConstructor(MysteryBoxclass, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    Object[] objects=param.args;
                    Log.d(tag,"beforeHookedMethod:objects length=" +objects.length);
//                    Log.d(tag, "beforeHookedMethod:price" + param.args[0]);
                    super.beforeHookedMethod(param);
                }
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                }

            });

            //第二种更简单的方法
            RposedHelpers.findAndHookConstructor("com.example.manghe.MysteryBox", lpparam.classLoader, int.class,String.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    Log.d(tag, "beforeHookedMethod:price=" + param.args[0]+param.args[1]);
                    param.args[0] =10000;
                    param.args[1] ="6666666666";
                    super.beforeHookedMethod(param);
                }
                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    Log.d(tag, "afterHookedMethod" +param.thisObject+param.getResult());
                    param.getResult();
                }

            });



            Log.i(tag, "hook end");
        }
    }

    private static void addFloatingButtonForActivity(final RC_LoadPackage.LoadPackageParam lpparam) {
        RposedHelpers.findAndHookMethod(Activity.class, "onCreate", Bundle.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(final MethodHookParam param) throws Throwable {
                new Handler(Looper.getMainLooper())
                        .postDelayed(new Runnable() {
                            @Override
                            public void run() {
                                createAndAttachFloatingButtonOnActivity((Activity) param.thisObject);
                            }
                        }, 1000);
            }

            private void createAndAttachFloatingButtonOnActivity(Activity activity) {
                Context context = RatelToolKit.ratelResourceInterface.createContext(lpparam.modulePath, HookEntry.class.getClassLoader(), RatelToolKit.sContext);

                FrameLayout frameLayout = (FrameLayout) activity.getWindow().getDecorView();
                LayoutInflater.from(context).cloneInContext(context)
                        .inflate(R.layout.float_button, frameLayout);

            }
        });
    }
}
