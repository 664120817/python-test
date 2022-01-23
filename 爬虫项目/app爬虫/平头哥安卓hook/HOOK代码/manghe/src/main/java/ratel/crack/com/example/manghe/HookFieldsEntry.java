package ratel.crack.com.example.manghe;

import android.util.Log;

import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;


public class HookFieldsEntry implements IRposedHookLoadPackage {
    private static final String tag = "DEMO_HOOK2";

    @Override
    public void handleLoadPackage(RC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if (lpparam.packageName.equals("com.example.manghe")) {
            Log.i(tag, "hook start2");
            Log.i(tag, "hook end2");

        }

        RposedHelpers.findAndHookConstructor("com.example.manghe.MysteryBox", lpparam.classLoader, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                super.afterHookedMethod(param);
                Object box = param.thisObject;
                Log.d(tag, "afterHookedMethod" +box);
                //获取实例属性
                Object content= RposedHelpers.getObjectField(box,"content");
                Log.d(tag, "afterHookedMethod获取到的content内容为"+content);
                int price=RposedHelpers.getIntField(box,"price");
                Log.d(tag, "afterHookedMethod获取到的price内容为"+price);

                //获取静态属性
                Object base_price= RposedHelpers.getObjectField(box.getClass(),"BASE_PRICE");
                Log.d(tag, "afterHookedMethod获取到的base_price内容为"+base_price);
                //修改实例属性
                RposedHelpers.setIntField(box,"price",1000);
                RposedHelpers.setObjectField(box,"content","惊喜款");
                //修改静态属性
                RposedHelpers.setStaticObjectField(box.getClass(),"BASE_PRICE",200);
                base_price = RposedHelpers.getStaticObjectField(box.getClass(),"BASE_PRICE");
                Log.d(tag, "afterHookedMethod获取到的修改静态属性base_price值"+base_price);

            }
        });

    }
}
