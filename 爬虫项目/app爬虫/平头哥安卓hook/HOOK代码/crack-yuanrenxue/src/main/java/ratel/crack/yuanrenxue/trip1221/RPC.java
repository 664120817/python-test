package ratel.crack.yuanrenxue.trip1221;

import android.app.Application;
import android.text.TextUtils;
import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.SimpleHttpInvoker;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.Constants;
import com.virjar.sekiro.api.SekiroClient;
import com.virjar.sekiro.api.SekiroResponse;

import java.util.Random;
import java.util.UUID;

import ratel.crack.yuanrenxue.trip1221.handlers.CtripEnglishHotelSearch;
import ratel.crack.yuanrenxue.trip1221.handlers.HotelDetailHandler;
import ratel.crack.yuanrenxue.trip1221.handlers.KeyWordSearchHandler;
import ratel.crack.yuanrenxue.trip1221.handlers.RatelPlanHandler;


public class RPC {
    public static void setupRPC() {
        //setupProxy();
        startRPC();
        //ensureApplicationCache();
    }

    private static void startRPC() {
        if (RatelToolKit.processName.equals(RatelToolKit.packageName)) {
            SekiroClient.start("sekiro.virjar.com", Constants.defaultNatServerPort,
                    UUID.randomUUID().toString(), "yrx-ctrip-english")
                    .registerHandler(new CtripEnglishHotelSearch())
                    .registerHandler(new KeyWordSearchHandler())
                    .registerHandler(new HotelDetailHandler())
                    .registerHandler(new RatelPlanHandler())
            ;
        }
    }

    private static void setupProxy() {
        if (RatelToolKit.packageName.equals(RatelToolKit.processName)) {
            final Object lock = new Object();
            new Thread("setup proxy") {
                @Override
                public void run() {
                    try {
                        String response = SimpleHttpInvoker.get("http://yourip.center.com/param");
                        if (response != null) {
                            String[] split = response.split("\n");
                            if (split.length > 0) {
                                String proxy = split[new Random().nextInt(split.length)];
                                Log.i(Trip1221.tag, "设置代理:" + proxy.trim());
                                // proxy = "192.168.0.2:8889";
                                System.setProperty("virjar-sockts-proxy", proxy.trim());
                            }
                        }
                    } finally {
                        synchronized (lock) {
                            lock.notify();
                        }
                    }
                }
            }.start();
            synchronized (lock) {
                try {
                    lock.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private static void ensureApplicationCache() {
        //e.h.e.q.e#b
        RposedHelpers.findAndHookMethod(
                RposedHelpers.findClass("e.h.e.q.e", RatelToolKit.hostClassLoader),
                "b", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Object b = RposedHelpers.getObjectField(param.thisObject, "b");
                        if (b != null) {
                            return;
                        }
                        if (RatelToolKit.sContext instanceof Application) {
                            param.setResult(RatelToolKit.sContext);
                        } else {
                            param.setResult(RatelToolKit.sContext.getApplicationContext());
                        }

                    }
                }
        );
    }


    public static void sendHotelBaseJavaRequest(Object hotelBaseJavaRequest, SekiroResponse sekiroResponse, String currency) {

        if (!TextUtils.isEmpty(currency)) {
            Object ibuHotelJavaHead = RposedHelpers.getObjectField(hotelBaseJavaRequest, "ibuRequestHead");
            RposedHelpers.setObjectField(ibuHotelJavaHead, "currency", currency);
        }

        Object ibuRequest = RposedHelpers.getObjectField(hotelBaseJavaRequest, "request");


        //e.h.e.t.n#a() e.h.e.t.n
        Object N = RposedHelpers.callStaticMethod(
                RposedHelpers.findClass("e.h.e.t.n", RatelToolKit.hostClassLoader),
                "a"
        );

        //请注意 buildNewCTHTTPRequest是通过rdp新增加的一个方法
        Object newCTHTTPRequest = RposedHelpers.callMethod(N, "buildNewCTHTTPRequest", ibuRequest, false);

        //FileLogger.outLog("virjar build newCTHTTPRequest:" + JSON.toJSONString(newCTHTTPRequest));


        // sekiroResponse.success(ForceFiledViewer.toView(newCTHTTPRequest));

        //ctrip.android.httpv2.CTHTTPClient#getInstance
        Object CTHTTPClient = RposedHelpers.callStaticMethod(
                RposedHelpers.findClass("ctrip.android.httpv2.CTHTTPClient", RatelToolKit.hostClassLoader)
                , "getInstance"
        );

        Object virjarCTHTTPCallback = RposedHelpers.newInstance(
                RposedHelpers.findClass("VirjarCTHTTPCallback", RatelToolKit.hostClassLoader),
                sekiroResponse
        );

        RposedHelpers.callMethod(CTHTTPClient, "sendRequest",
                newCTHTTPRequest, virjarCTHTTPCallback);
    }

    static {
        RposedHelpers.findAndHookMethod(
                RposedHelpers.findClass("VirjarCTHTTPCallback",
                        RatelToolKit.hostClassLoader),
                "onResponse",
                "ctrip.android.httpv2.CTHTTPResponse", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) {
                        SekiroResponse sekiroResponse = RposedHelpers.getObjectField(param.thisObject, "obj");

                        Object responseBean = RposedHelpers.getObjectField(param.args[0], "responseBean");

                        sekiroResponse.success(responseBean);
                    }
                }
        );

        RposedHelpers.findAndHookMethod(
                RposedHelpers.findClass("VirjarCTHTTPCallback",
                        RatelToolKit.hostClassLoader),
                "onError",
                "ctrip.android.httpv2.CTHTTPError", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        SekiroResponse sekiroResponse = RposedHelpers.getObjectField(param.thisObject, "obj");
                        sekiroResponse.failed(param.args[0].toString());
                    }
                }
        );
    }
}
