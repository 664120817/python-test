package ratel.crack.yuanrenxue.trip1221.pages;

import android.app.Activity;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

public class LoginTypeActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        return root.clickByXpath("//android.widget.Button[@id='ctrip.english:id/main_login_btn']");
    }
}
