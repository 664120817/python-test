package ratel.com.csair.mbp.page;

import android.app.Activity;
import android.text.TextUtils;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

import ratel.com.csair.mbp.Account;

public class CSMBPActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {

    //private boolean isFirst = true;

    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
//        if (isFirst) {
//            isFirst = false;
//            //首次进入首页，等待3s
//            PageTriggerManager.trigger(3000);
//            return true;
//        }


        if (!needLogin()) {
            FileLogger.outLog("已经登录了，不需要登录");
            return true;
        }


        ViewImage loginBtn = root.xpath2One("//android.widget.TextView[@id='com.csair.mbp:id/tv_login_context' and @shown]");
        if (loginBtn == null) {
            root.clickByXpath("//android.widget.TextView[@id='com.csair.mbp:id/main_mine_txt']");
            PageTriggerManager.trigger();
            return true;
        } else {
            loginBtn.click();
        }
        return false;
    }

    private boolean needLogin() {
        FileLogger.outLog("LoginInfoTempFile:" + Account.getLoginTempFile());
        if (!TextUtils.isEmpty(Account.getLoginUserId())) {
            //已经登录了
            return false;
        }
        return !TextUtils.isEmpty(Account.userName);
    }


}
