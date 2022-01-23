package ratel.com.csair.mbp.services;

import android.os.Handler;
import android.os.Looper;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.inspect.Lists;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import external.com.alibaba.fastjson.JSON;
import external.com.alibaba.fastjson.JSONArray;
import external.com.alibaba.fastjson.JSONObject;
import external.com.alibaba.fastjson.serializer.SerializerFeature;
import ratel.com.csair.mbp.Account;
import ratel.com.csair.mbp.beans.PassengerAdaptor;
import ratel.com.csair.mbp.beans.PassengerModel;
import ratel.com.csair.mbp.utils.OrderLogger;

public class PassengerCacheServices {
    public static Map<String, JSONObject> cachedPassenger = new ConcurrentHashMap<>();

    private static boolean fired = false;

    private static final Object lock = new Object();

    public static List<JSONObject> getSubmitPassenger() {
        if (cachedPassenger.size() == ConfigManager.getInstance().getPassengerList().size()) {
            return Lists.newArrayList(cachedPassenger.values());
        }
        startCache();
        synchronized (lock) {
            try {
                lock.wait(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        if (cachedPassenger.size() == ConfigManager.getInstance().getPassengerList().size()) {
            return Lists.newArrayList(cachedPassenger.values());
        }
        return null;
    }

    public static void startCache() {
        if (fired) {
            return;
        }
        if (!Account.isLogin()) {
            return;
        }

        final JSONObject userInfo = Account.getLoginTempFile();

        JSONObject queryPassengerRequest = new JSONObject();
        queryPassengerRequest.put("aid", userInfo.getString("CARD_NO"));
        queryPassengerRequest.put("flightRegion", "1");
        //{"aid":"113164642916","flightRegion":"1"}
        NetworkServices.sendPostRequest(
                "https://3g.csair.com/CSMBP/data/order/account/findPassengerList.do",
                queryPassengerRequest.toJSONString(), new NetworkServices.NetworkCallback() {
                    @Override
                    public void onSuccess(String body) {

                        JSONArray passengers = JSON.parseObject(body).getJSONArray("passengers");
                        Map<String, JSONObject> existedPassengerMap = new HashMap<>();
                        for (int i = 0; i < passengers.size(); i++) {
                            existedPassengerMap
                                    .put(passengers.getJSONObject(i).getString("certNum").toUpperCase(),
                                            passengers.getJSONObject(i));
                        }

                        List<ConfigManager.PassengerBean> passengerList = ConfigManager.getInstance().getPassengerList();

                        for (ConfigManager.PassengerBean passengerBean : passengerList) {
                            String certNumber = passengerBean.certNumber.toUpperCase();
                            if (existedPassengerMap.containsKey(certNumber)) {
                                cachedPassenger.put(certNumber, existedPassengerMap.get(certNumber));
                            } else {
                                addPassenger(passengerBean, userInfo.getString("CARD_NO"));
                            }
                        }
                        if (cachedPassenger.size() == ConfigManager.getInstance().getPassengerList().size()) {
                            synchronized (lock) {
                                lock.notifyAll();
                            }
                        }
                    }

                    @Override
                    public void onFiled(Exception e) {
                        ActivityHooker.appendPanel("查询乘机人失败:" + e.getMessage());
                        fired = false;
                        new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
                            @Override
                            public void run() {
                                startCache();
                            }
                        }, 5000);
                    }
                }
        );


        fired = true;
    }


    private static void addPassenger(final ConfigManager.PassengerBean passenger, final String ffpCardno) {
        PassengerModel passengerModel = new PassengerModel(
                passenger.birthday,
                passenger.cardIssuePlace,
                passenger.certNumber,
                passenger.certExpireDate,
                PassengerAdaptor.getIdType(passenger.certType),
                PassengerAdaptor.getSexType(passenger.gender),
                !passenger.getIsChild(),
                passenger.cardIssuePlace,
                passenger.userName,
                ffpCardno);

        NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/account/modifyPassengerInfo",
                JSON.toJSONString(passengerModel, SerializerFeature.WriteMapNullValue),
                new NetworkServices.NetworkCallback() {
                    @Override
                    public void onSuccess(String body) {
                        OrderLogger.outLog("乘机人添加结果:" + body);
                        JSONObject vo = JSONObject.parseObject(body).getJSONObject("vo");
                        String certNum = vo.getString("certNum");
                        cachedPassenger.put(certNum.toUpperCase(), vo);

                        if (cachedPassenger.size() == ConfigManager.getInstance().getPassengerList().size()) {
                            synchronized (lock) {
                                lock.notifyAll();
                            }
                        }
                    }

                    @Override
                    public void onFiled(Exception e) {
                        String errorMsg = "添加乘机人失败:" + JSONObject.toJSONString(passenger) + " stack: " + FileLogger.getTrack(e);
                        OrderLogger.outLog(errorMsg);
                        FileLogger.outLog(errorMsg);
                        ActivityHooker.appendPanel("添加乘机人失败:" + e.getMessage());
                        new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
                            @Override
                            public void run() {
                                addPassenger(passenger, ffpCardno);
                            }
                        }, 5000);
                    }
                }
        );
    }
}
