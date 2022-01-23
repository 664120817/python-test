package ratel.crack.com.example.manghe;

import android.util.Log;

import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;

import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;


public class HookMethodsEntry implements IRposedHookLoadPackage {
    private static final String tag = "DEMO_HOOK3";

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (lpparam.packageName.equals("com.example.manghe")) {
            Log.i(tag, "hook start3");

// hook 静态方法
            RposedHelpers.findAndHookMethod("com.example.manghe.MysteryBox", lpparam.classLoader, "staticMethod", String.class, int.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                    //获取方法参数
                    Log.d(tag, "beforeHookedMethod:args[0]="+param.args[0]+"args[1]:"+param.args[1]);
                    //对于方法参数修改
                    param.args[0] ="修改的第一个静态方法";
                    param.args[1]= 500;

                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    //获取方法返回值
                    Object result = param.getResult();
                    Log.d(tag, "afterHookedMethod result:"+result);
                    //修改方法返回值，和原始返回值类型要一致
                    param.setResult("我是修改之后的静态方法返回值");
                }
            });

//Hook实例方法
            RposedHelpers.findAndHookMethod("com.example.manghe.MysteryBox", lpparam.classLoader, "instanceMethod", String.class, int.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                    //获取方法参数
                    Log.d(tag, "beforeHookedMethod:args[0]="+param.args[0]+"args[1]:"+param.args[1]);
                    //对于方法参数修改
                    param.args[0] ="实例参数";
                    param.args[1]= 5000;
                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    param.setResult("我是修改之后的实例方法返回值");
                }
            });
//内部内处理
            RposedHelpers.findAndHookMethod("com.example.manghe.MysteryBox$InnerClass", lpparam.classLoader, "innerClassMethod", String.class, int.class, new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);
                    //获取方法参数
                    Log.d(tag, "beforeHookedMethod:args[0]="+param.args[0]+"args[1]:"+param.args[1]);
                    //对于方法参数修改
                    param.args[0] ="内部内参数";
                    param.args[1]= 5000;
                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    param.setResult("我是修改之后的内部内方法返回值");
                }
            });


            //hook native 函数
            RposedHelpers.findAndHookMethod("com.example.manghe.MainActivity", lpparam.classLoader, "nativeMathod", new RC_MethodHook() {
                @Override
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                    super.beforeHookedMethod(param);

                    Log.d(tag, "beforeHookedMethod nativeMathod:="+param.args.length);

                }

                @Override
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                    super.afterHookedMethod(param);
                    Log.d(tag, "afterHookedMethod nativeMathod getResult:="+param.getResult());
                    param.setResult("我是修改之后的native方法返回值");



                }
            });

        }

        Log.i(tag, "hook end3");
    }

}
