package ratel.com.csair.mbp.page;

import android.app.Activity;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

public class WelcomeActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        ViewImage viewImage = root.xpath2One("//android.widget.Button[@id='com.csair.mbp:id/privacy_confirm_bt']");
        if (viewImage != null) {
            viewImage.click();
            return false;
        }
        viewImage = root.xpath2One("//android.widget.Button[@id='com.csair.mbp:id/authority_confirm_bt']");
        if (viewImage != null) {
            viewImage.click();
            return false;
        }
        return false;
    }
}
