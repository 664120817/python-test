package ratel.com.csair.mbp.sekiro;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;

import java.io.File;
import java.io.IOException;

import ratel.com.csair.mbp.Account;
import ratel.com.csair.mbp.utils.OrderLogger;

public class LogViewAction implements ActionHandler {
    @Override
    public String action() {
        return "logView";
    }

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
        File logFile = OrderLogger.getLogFile();
        if (logFile == null) {
            sekiroResponse.failed("no data");
            return;
        }
        FileLogger.outLog("当前设备id:" + Account.getLoginUserId());
        try {
            sekiroResponse.sendFile(logFile);
        } catch (IOException e) {
            sekiroResponse.failed("failed to read file: " + logFile.getAbsolutePath() + FileLogger.getTrack(e));
        }
    }
}
