package com.virjar.ratel.snkrs.pages;

import android.app.Activity;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

public class TheWallActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        return root.clickByXpath("//android.widget.Button[@id='com.nike.snkrs:id/loginButton']");
    }
}
