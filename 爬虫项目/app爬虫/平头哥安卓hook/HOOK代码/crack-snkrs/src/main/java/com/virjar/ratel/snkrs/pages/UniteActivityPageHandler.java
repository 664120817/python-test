package com.virjar.ratel.snkrs.pages;

import android.app.Activity;
import android.util.Log;
import android.webkit.WebView;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;
import com.virjar.ratel.api.extension.superappium.WebViewHelper;
import com.virjar.ratel.snkrs.GrabTaskBean;
import com.virjar.ratel.snkrs.HookEntry;

public class UniteActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        WebView webView = root.findWebViewIfExist();
        if (webView == null) {
            Log.i(HookEntry.TAG, "无法定位登陆WebView...");
            return false;
        }
        WebViewHelper.JsCallFuture jsCallFuture = new WebViewHelper(webView).typeByXpath("//input[@data-componentname='phoneNumber']", GrabTaskBean.userName);

        jsCallFuture.success()
                .typeByXpath("//input[@data-componentname='password']", GrabTaskBean.password)
                .clickByXpath("//input[@type='button' and @value='登录']");

        jsCallFuture.failed(new WebViewHelper.OnJsCallFinishEvent() {
            @Override
            public void onJsCallFinished(String callResultId) {
                PageTriggerManager.trigger(400);
            }
        });

        return true;
    }
}

