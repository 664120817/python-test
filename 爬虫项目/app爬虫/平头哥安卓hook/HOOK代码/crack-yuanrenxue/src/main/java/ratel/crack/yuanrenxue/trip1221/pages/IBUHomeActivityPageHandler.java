package ratel.crack.yuanrenxue.trip1221.pages;

import android.app.Activity;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.util.Log;
import android.view.View;
import android.view.Window;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SwipeUtils;
import com.virjar.ratel.api.extension.superappium.ViewImage;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RposedHelpers;

import java.util.concurrent.ThreadLocalRandom;

import external.com.alibaba.fastjson.JSON;
import ratel.crack.yuanrenxue.trip1221.Trip1221;


public class IBUHomeActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {

        Window topDialogWindow = PageTriggerManager.getTopDialogWindow();
        if (topDialogWindow != null) {
            ViewImage dialogDomRoot = new ViewImage(topDialogWindow.getDecorView());
            ViewImage okbutton = dialogDomRoot.xpath2One("//android.widget.Button[@text='好的' and @visible]");
            if (okbutton != null) {
                okbutton.click();
                PageTriggerManager.trigger();
                return true;
            }
        }

        //在启动页
        ViewImage splashDom = root.xpath2One("//android.widget.Button[@text='開始體驗！']");
        if (splashDom != null) {
            //开始体验
            ViewImage startButton = root.xpath2One("//android.widget.Button[@text='開始體驗！' and @visible]");
            if (startButton == null) {
                Log.i(Trip1221.tag, "左滑..");
                swipeRight(root.getOriginView(), root, -400);
                PageTriggerManager.trigger(1200);
                return false;
            } else {
                Log.i(Trip1221.tag, "找到【开始体验】按钮，点击按钮进入下一个页面 ");
                startButton.click();
                return false;
            }
        }

        Class<?> userManagerClass = RposedHelpers.findClass("e.h.e.a.a.e.e", RatelToolKit.hostClassLoader);
        Object userManager = RposedHelpers.callStaticMethod(userManagerClass, "y");
        Object memberInfo = RposedHelpers.callMethod(userManager, "l");
        Log.i(Trip1221.tag, "当前账户信息:" + JSON.toJSONString(ForceFiledViewer.toView(memberInfo)) + " isNull?" + (memberInfo == null));

        if (memberInfo == null) {
            Log.i(Trip1221.tag, "当前设备没有登录账号");
            ViewImage loginButton = root.xpath2One("//android.widget.Button[@id='ctrip.english:id/unlogin_tvSignIn' and @visible]");
            if (loginButton != null) {
                Log.i(Trip1221.tag, "点击登录/注册按钮，准备进入登录界面");
                return loginButton.click();
            }
            // 登录
            ViewImage accountTab = root.xpath2One("//android.widget.TextView[@id='ctrip.english:id/accountTab']");
            if (accountTab != null) {
                Log.i(Trip1221.tag, "点击底部账户tab，准备进入登录逻辑");
                accountTab.click();
                PageTriggerManager.trigger();
                return false;
            }
        }




        return false;
    }

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    private static void swipeRight(View originView, ViewImage root, int width) {
        int[] locs = new int[2];
        originView.getLocationOnScreen(locs);

        int viewWidth = originView.getWidth();
        int viewHeight = originView.getHeight();

        int fromY = (int) (locs[1] + viewHeight * (ThreadLocalRandom.current().nextDouble(0.05) - 0.025 + 0.5));
        if (fromY < 2) {
            fromY = 2;
        }
        int toY = (int) (fromY + viewHeight * (ThreadLocalRandom.current().nextDouble(0.008)));

        int fromX, toX;

        if (width > 0) {
            fromX = (int) (locs[0] + viewWidth * ThreadLocalRandom.current().nextDouble(0.1));
            if (fromX < 2) {
                fromX = 2;
            }
            toX = fromX + width;
        } else {
            fromX = (int) (locs[0] + viewWidth * (ThreadLocalRandom.current().nextDouble(0.1) + 0.9));
            toX = fromX + width;
            if (toX < 2) {
                toX = 2;
            }
        }
//        Log.i(SuperAppium.TAG, "location on screen: (" + locs[0] + "," + locs[1] + ")  from loc:("
//                + fromX + "," + fromY + ") to loc:(" + toX + "," + toY + ") with and height: (" + viewWidth + "," + viewHeight + ")");
        SwipeUtils.simulateScroll(root, fromX, fromY, toX, toY, 300, 30);
    }
}
