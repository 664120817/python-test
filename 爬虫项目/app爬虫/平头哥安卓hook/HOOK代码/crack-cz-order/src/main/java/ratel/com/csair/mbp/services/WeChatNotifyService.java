package ratel.com.csair.mbp.services;

import org.joda.time.DateTime;

import java.net.URLEncoder;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import ratel.com.csair.mbp.SimpleCZHttpInvoker;

public class WeChatNotifyService {

    private static ExecutorService executorService = Executors.newSingleThreadExecutor();

    private static final String baseURL = "https://sekiro.virjar.com/invoke?group=1234535d&action=sendMessage&receiverNickname=%E6%9C%BA%E7%A5%A8%E9%80%9A%E7%9F%A5%E7%BE%A4&content=";


    public static void sendWechatNotify(final String message) {
        executorService.submit(new Runnable() {
            @Override
            public void run() {
                ConfigManager.TripBean tripConfig = ConfigManager.getInstance().getTripConfig();
                for (int i = 0; i < 3; i++) {
                    String response = SimpleCZHttpInvoker.get(baseURL + URLEncoder.encode(
                            "离线生单:\n" +
                                    "" + tripConfig.dep + " -> " + tripConfig.arr + " : " + tripConfig.flightNumber +
                                    " " + tripConfig.depDate + "\n" +
                                    "当前设备:" + ConfigManager.getInstance().getSetting().clientId + "\n"
                                    + "当前时间:" + DateTime.now().toString("yyyy-MM-dd HH:mm:ss") + "\n"
                                    + message));
                    if (response != null) {
                        break;
                    }
                }
            }
        });
    }


}
