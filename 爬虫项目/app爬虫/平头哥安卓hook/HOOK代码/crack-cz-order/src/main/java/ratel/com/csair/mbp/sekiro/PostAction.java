package ratel.com.csair.mbp.sekiro;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import external.com.alibaba.fastjson.JSON;
import ratel.com.csair.mbp.services.NetworkServices;

public class PostAction implements ActionHandler {
    @Override
    public String action() {
        return "booking";
    }

    @AutoBind
    private String url;

    @AutoBind
    private String body;


    @Override
    public void handleRequest(final SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {

        NetworkServices.sendPostRequest(url, body, new NetworkServices.NetworkCallback() {
            @Override
            public void onSuccess(String body) {
                sekiroResponse.success(JSON.parse(body));
            }

            @Override
            public void onFiled(Exception e) {
                sekiroResponse.failed(FileLogger.getTrack(e));
            }
        });
    }
}
