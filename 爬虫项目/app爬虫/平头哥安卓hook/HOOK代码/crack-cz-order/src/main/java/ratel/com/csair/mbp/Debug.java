package ratel.com.csair.mbp;

import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.UnPackerToolKit;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

import java.io.File;
import java.io.IOException;

import ratel.com.csair.mbp.utils.FileUtils;

public class Debug {
    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {
        if (lpparam.packageName.equals(lpparam.processName)) {


//            PageTriggerManager.getTopDialogWindow();
//            SekiroStarter.startService("sekiro.virjar.com", Constants.defaultNatServerPort,
//                    "yuanrenxue-cz");

        }
    }

    private static void unpack() {
        final UnPackerToolKit.UnpackEvent unpackEvent = new UnPackerToolKit.UnpackEvent() {
            @Override
            public void onFinish(File file) {
                try {
                    Log.e(HookEntry.TAG, "unpack finished!!");
                    FileUtils.copyFile(file, new File(RatelToolKit.whiteSdcardDirPath, "cz_unpack.apk"));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };
        RatelToolKit.ratelUnpack.enableUnPack(new File(RatelToolKit.whiteSdcardDirPath, "ratel_unpack"), false);
        UnPackerToolKit.unpack(unpackEvent);
    }
}
