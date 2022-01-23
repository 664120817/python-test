package ratel.com.csair.mbp.sekiro;

import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;

import external.com.alibaba.fastjson.JSONObject;
import ratel.com.csair.mbp.Account;
import ratel.com.csair.mbp.services.NetworkServices;

public class MUserInfoAction implements ActionHandler {
    @Override
    public String action() {
        return "userInfo";
    }

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
        if (!NetworkServices.isReady()) {
            sekiroResponse.failed("the app not ready");
            return;
        }
        JSONObject loginTempFile = Account.getLoginTempFile();
        if (loginTempFile == null) {
            sekiroResponse.failed("not login");
        } else {
            sekiroResponse.success(loginTempFile);
        }
    }
}
