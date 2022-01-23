package ratel.com.csair.mbp.sekiro;

import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.zip.GZIPInputStream;

import ratel.com.csair.mbp.HookEntry;

public class DecodeAction implements ActionHandler {

    @AutoBind
    private String param;

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {

        Class<?> clazz = RposedHelpers.findClass("com.csair.mbp.j.a.a", RatelToolKit.hostClassLoader);
        Log.e(HookEntry.TAG, "待解密字符串: " + param);
        Object instance2 = RposedHelpers.newInstance(clazz, RatelToolKit.sContext);
        byte[] bytes = (byte[]) RposedHelpers.callMethod(instance2, "a", param);//解密字符串
        String decodeResultStr = uncompressToString(bytes, "utf-8");
        Log.e(HookEntry.TAG, "解密结果==>" + decodeResultStr);
        sekiroResponse.success(decodeResultStr);
    }

    private static String uncompressToString(byte[] bytes, String encoding) {
        if (bytes == null || bytes.length == 0) {
            return null;
        }
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayInputStream in = new ByteArrayInputStream(bytes);
        try {
            GZIPInputStream ungzip = new GZIPInputStream(in);
            byte[] buffer = new byte[256];
            int n;
            while ((n = ungzip.read(buffer)) >= 0) {
                out.write(buffer, 0, n);
            }
            return out.toString(encoding);
        } catch (IOException e) {

        }
        return null;
    }


    @Override
    public String action() {
        return "decode";
    }
}
