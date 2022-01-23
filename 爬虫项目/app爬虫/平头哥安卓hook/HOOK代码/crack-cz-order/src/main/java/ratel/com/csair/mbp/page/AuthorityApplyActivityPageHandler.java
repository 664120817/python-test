package ratel.com.csair.mbp.page;

import android.app.Activity;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

public class AuthorityApplyActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        root.clickByXpath("//android.widget.Button[@id='com.csair.mbp:id/authority_confirm_bt']");
        return false;
    }
}
