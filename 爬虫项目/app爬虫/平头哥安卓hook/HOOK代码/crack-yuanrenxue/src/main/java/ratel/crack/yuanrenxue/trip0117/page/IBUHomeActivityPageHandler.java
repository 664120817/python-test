package ratel.crack.yuanrenxue.trip0117.page;

import android.app.Activity;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.util.Log;
import android.view.View;
import android.view.Window;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SwipeUtils;
import com.virjar.ratel.api.extension.superappium.ViewImage;

import java.util.concurrent.ThreadLocalRandom;

import ratel.crack.yuanrenxue.trip0117.Trip0117;
import ratel.crack.yuanrenxue.trip1221.Trip1221;

public class IBUHomeActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        Log.i(Trip0117.tag, "in activity: " + activity.getClass());

        Window topDialogWindow = PageTriggerManager.getTopDialogWindow();
        if (topDialogWindow != null) {
            ViewImage dialogRoot = new ViewImage(topDialogWindow.getDecorView());
            ViewImage okBtn = dialogRoot.xpath2One("//android.widget.Button[@id='ctrip.english:id/allowButton'  and @text='好的']");
            if (okBtn != null) {
                Log.i(Trip0117.tag, "点击弹窗");
                okBtn.click();
                return false;
            }
        }

        ViewImage viewImage = root.xpath2One("//android.widget.TextView[@id='ctrip.english:id/title' and @visible]");
        if (viewImage != null) {
            Log.i(Trip0117.tag, "首屏滑动");
            String text = viewImage.getText();
            if (!"酒店".equals(text)
                    && !"機票".equals(text)
                    && !"火車票".equals(text)
            ) {
                swipeRight(viewImage.getOriginView(), root, -400);
                PageTriggerManager.trigger(1200);
                return true;
            }


        }

        ViewImage startBtn = root.xpath2One("//android.widget.Button[@id='ctrip.english:id/tvGet' and @text='開始體驗！']");
        if (startBtn != null) {
            Log.i(Trip0117.tag, "点击开始体验");
            startBtn.click();
            return false;
        }

        ViewImage loginButton = root.xpath2One("//android.widget.Button[@id='ctrip.english:id/unlogin_tvSignIn' and @visible]");
        if (loginButton != null) {
            Log.i(Trip1221.tag, "点击登录/注册按钮，准备进入登录界面");
            loginButton.click();
            return false;
        }

        // 判断是否需要登录
        ViewImage needLogin = root.xpath2One("//android.widget.Button[@text='立即登入' and @visible]");
        if (needLogin != null) {
            Log.i(Trip0117.tag, "点击账户tab");
            root.clickByXpath("//android.widget.TextView[@id='ctrip.english:id/accountTab']");
            return false;
        }

        return true;
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
