package ratel.com.csair.mbp.sekiro;

import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import ratel.com.csair.mbp.HookEntry;

public class EncodeAction implements ActionHandler {

    @AutoBind
    private String param;

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {

        Class<?> clazz = RposedHelpers.findClass("com.csair.mbp.j.a.a", RatelToolKit.hostClassLoader);
        Object instance = RposedHelpers.newInstance(clazz, RatelToolKit.sContext);
        String encodeResultStr = (String) RposedHelpers.callMethod(instance, "b", param);//加密字符串
        sekiroResponse.success(encodeResultStr);
        Log.d(HookEntry.TAG, "加密结果==>" + encodeResultStr);
    }

    @Override
    public String action() {
        return "encode";
    }
}
