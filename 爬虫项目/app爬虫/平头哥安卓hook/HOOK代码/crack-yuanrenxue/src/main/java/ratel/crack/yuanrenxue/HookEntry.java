package ratel.crack.yuanrenxue;

import com.virjar.ratel.api.rposed.IRposedHookLoadPackage;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;

import ratel.crack.yuanrenxue.baidu0103.BaiduMap0103;
import ratel.crack.yuanrenxue.pdd0302.PddEntry;
import ratel.crack.yuanrenxue.trip0117.Trip0117;
import ratel.crack.yuanrenxue.xhs0411.XHS0411;

/**
 * Created by virjar on 2018/10/6.
 */

public class HookEntry implements IRposedHookLoadPackage {

    @Override
    public void handleLoadPackage(final RC_LoadPackage.LoadPackageParam lpparam) {
        if (lpparam.packageName.equals("com.fgsdfasd.midou")) {
            MidouEntry.entry(lpparam);
        } else if (lpparam.packageName.equals("ctrip.english")) {
            //TripHookEntry.entry(lpparam);
            Trip0117.entry(lpparam);
        } else if (lpparam.packageName.equals("com.baidu.BaiduMap")) {
            // BaiduEntry.entry(lpparam);
            BaiduMap0103.entry(lpparam);
        } else if (lpparam.packageName.equals("com.xunmeng.pinduoduo")) {
            PddEntry.entry(lpparam);
        } else if (lpparam.packageName.equals("com.xingin.xhs")) {
            XHS0411.entry(lpparam);
        }
    }

}
