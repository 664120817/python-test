package ratel.com.csair.mbp.page;

import android.app.Activity;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

public class UpdateActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        ViewImage closeUpdateIcon = root.xpath2One("//android.widget.ImageView[@id='com.csair.mbp:id/activity_update_iv_close']");
        if (closeUpdateIcon != null) {
            closeUpdateIcon.click();
            return true;
        }
        return false;
    }
}
