package ratel.crack.yuanrenxue.trip1221.pages;

import android.app.Activity;
import android.text.TextUtils;
import android.util.Log;

import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.ViewImage;

import ratel.crack.yuanrenxue.trip1221.Trip1221;


public class LoginActivityPageHandler implements PageTriggerManager.ActivityFocusHandler {
    @Override
    public boolean handleActivity(Activity activity, ViewImage root) {

        String accountText = root.xpath2String("//android.widget.EditText[@id='ctrip.english:id/auto_complete_bottom' and @hint='電郵/用戶名/電話號碼' and @visible ]/@text");
        Log.i(Trip1221.tag, "当前账户：" + accountText);
        if (TextUtils.isEmpty(accountText)) {
            Log.i(Trip1221.tag, "输入账户名..");
            root.typeByXpath("//android.widget.EditText[@id='ctrip.english:id/auto_complete_bottom' and @hint='電郵/用戶名/電話號碼' and @visible ]", "1106847522@qq.com");
            PageTriggerManager.trigger();
            return true;
        }

        String pwdText = root.xpath2String("//android.widget.EditText[@id='ctrip.english:id/auto_complete_bottom' and @hint='密碼' and @visible]/@text");
        if (TextUtils.isEmpty(pwdText)) {
            Log.i(Trip1221.tag, "输入密码..");
            root.typeByXpath("//android.widget.EditText[@id='ctrip.english:id/auto_complete_bottom' and @hint='密碼' and @visible ]", "qazwsx123");
            PageTriggerManager.trigger();
            return true;
        }
        return root.clickByXpath("//android.widget.Button[@id='ctrip.english:id/login_btn' and @visible]");
    }
}
