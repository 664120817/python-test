package ratel.crack.yuanrenxue;

import android.util.Log;

import com.virjar.ratel.api.UnPackerToolKit;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

import java.io.File;
import java.io.IOException;

import external.org.apache.commons.io.FileUtils;

public class MidouEntry {
    public static final String tag = "MIDOU";

    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {

        UnPackerToolKit.autoEnable(true);

        UnPackerToolKit.unpack(new UnPackerToolKit.UnpackEvent() {
            @Override
            public void onFinish(File file) {
                try {
                    FileUtils.copyFile(file, new File("/sdcard/midou-unpack.apk"));
                } catch (IOException e) {
                    Log.e(tag, "unpacked error", e);
                    e.printStackTrace();
                }
            }
        });
    }
}
