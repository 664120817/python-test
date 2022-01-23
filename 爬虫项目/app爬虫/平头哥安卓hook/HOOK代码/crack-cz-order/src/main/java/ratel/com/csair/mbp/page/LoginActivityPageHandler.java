package ratel.com.csair.mbp.page;

import android.app.Activity;
import android.widget.CheckBox;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

import external.org.apache.commons.lang3.StringUtils;
import ratel.com.csair.mbp.Account;

public class LoginActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {
        if (StringUtils.isBlank(Account.userName)) {
            FileLogger.outLog("不需要登录");
            return true;
        }
        String nowAccount = root.xpath2String("//android.widget.EditText[@id='com.csair.mbp:id/activity_login_et_member_account']/@text");
        FileLogger.outLog("当前账号:" + nowAccount);
        if (!StringUtils.equals(nowAccount, Account.userName)) {
            FileLogger.outLog("当前账号： " + nowAccount + " 待输入账号：" + Account.userName + " 输入账号");
            root.typeByXpath("//android.widget.EditText[@id='com.csair.mbp:id/activity_login_et_member_account']", Account.userName);
            PageTriggerManager.trigger();
            return true;
        }

        String nowPassword = root.xpath2String("//android.widget.EditText[@id='com.csair.mbp:id/activity_login_et_member_password_id']/@text");
        FileLogger.outLog("当前密码:" + nowPassword);
        if (nowPassword == null || nowPassword.length() < Account.password.length()) {
            FileLogger.outLog("当前密码： " + nowPassword + " 待输入密码：" + Account.password + " 输入密码");
            root.typeByXpath("//android.widget.EditText[@id='com.csair.mbp:id/activity_login_et_member_password_id']", Account.password);
            PageTriggerManager.trigger();
            return true;
        }

        ViewImage checkbox = root.xpath2One("//android.widget.CheckBox[@id='com.csair.mbp:id/activity_login_privacy_policy']");
        if (checkbox == null) {
            FileLogger.outLog("未找到隐私通知chekcbox");
            return false;
        }

        CheckBox c = (CheckBox) checkbox.getOriginView();
        if (!c.isChecked()) {
            FileLogger.outLog("点击隐私通知checkbox");
            c.performClick();
            PageTriggerManager.trigger();
            return true;
        }

        FileLogger.outLog("点击登录按钮");
        root.clickByXpath("//android.widget.Button[@id='com.csair.mbp:id/activity_login_btn_login_button']");

        return true;
    }
}
