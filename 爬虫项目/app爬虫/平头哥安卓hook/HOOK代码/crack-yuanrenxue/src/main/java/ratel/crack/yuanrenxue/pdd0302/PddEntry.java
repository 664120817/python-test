package ratel.crack.yuanrenxue.pdd0302;

import android.content.Intent;
import android.os.Parcel;
import android.util.Log;
import android.widget.TextView;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.log.SekiroLogger;

import external.com.alibaba.fastjson.JSONObject;

public class PddEntry {
    public static String tag = "PDD_HOOK";

    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {
        SekiroLogger.tag = tag;
        SuperAppium.TAG = tag;
        if (lpparam.processName.equals(lpparam.packageName)) {

        }

        Log.i(tag, "HOOK end!!");
    }

    public static void loge(String tag, String msg) {
        if (tag == null || tag.length() == 0 || msg == null || msg.length() == 0) {
            return;
        }
        int segmentSize = 3 * 1024;
        long length = msg.length();
        if (length <= segmentSize) {// 长度小于等于限制直接打印
            Log.e(tag, msg);
        } else {
            while (msg.length() > segmentSize) {// 循环分段打印日志
                String logContent = msg.substring(0, segmentSize);
                msg = msg.replace(logContent, "");
                Log.i(tag, logContent);
            }
            Log.i(tag, msg);// 打印剩余日志
        }

    }

}
