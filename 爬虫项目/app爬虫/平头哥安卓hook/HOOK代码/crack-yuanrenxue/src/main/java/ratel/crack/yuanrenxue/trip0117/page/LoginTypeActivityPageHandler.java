package ratel.crack.yuanrenxue.trip0117.page;

import android.app.Activity;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

public class LoginTypeActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        root.clickByXpath("//android.widget.Button[@id='ctrip.english:id/main_login_btn']");
        return true;
    }
}
