package ratel.com.csair.mbp.services;

import android.text.TextUtils;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.inspect.Lists;

import org.joda.time.DateTime;

import java.util.HashSet;
import java.util.List;

import external.com.alibaba.fastjson.JSON;
import external.com.alibaba.fastjson.JSONArray;
import external.com.alibaba.fastjson.JSONException;
import external.com.alibaba.fastjson.JSONObject;
import external.org.apache.commons.lang3.StringUtils;
import ratel.com.csair.mbp.Account;
import ratel.com.csair.mbp.beans.PassengerNum;
import ratel.com.csair.mbp.utils.OrderLogger;


public class OrderServices {

    private static boolean isOrder = false;
    private static long orderStart = -1;
    private static boolean running = true;
    private static Thread thread = new Thread("order") {
        @Override
        public void run() {
            try {
                //先等5s在搞事情
                Thread.sleep(8000);
            } catch (InterruptedException e) {
                FileLogger.outLog("error: " + FileLogger.getTrack(e));

            }
            while (running) {
                long sleep = 1000;
                if (isOrder) {
                    sleep = 20000;
                } else {
                    try {
                        sleep = runOrder();
                    } catch (Throwable e) {
                        FileLogger.outLog("error: " + FileLogger.getTrack(e));
                    }
                }
                if (sleep < 100) {
                    sleep = 100;
                }
                try {
                    Thread.sleep(sleep);
                } catch (InterruptedException e) {
                    FileLogger.outLog("error: " + FileLogger.getTrack(e));
                    break;
                }
            }
        }
    };

    public static void start() {
        if (!thread.isAlive()) {
            thread.start();
        }
    }


    private static long runOrder() {

        if (!ConfigManager.getInstance().getAccountList().isEmpty()
                && !Account.isLogin()
        ) {
            ActivityHooker.updatePanel("等待登录");
            return 5000;
        }

        ConfigManager.TripBean tripConfig = ConfigManager.getInstance().getTripConfig();
        if (TextUtils.isEmpty(tripConfig.dep) || TextUtils.isEmpty(tripConfig.arr)) {
            ActivityHooker.updatePanel("未设置出发到达");
            return 10000;
        }
        if (ConfigManager.getInstance().getTripConfig().ok) {
            ActivityHooker.updatePanel("当前订单已经完成");
            return 10000;
        }

        String contact = ConfigManager.getInstance().getContact().email;
        if (StringUtils.isNotBlank(contact)
                && !contact.contains("@")) {
            ActivityHooker.updatePanel("联系人邮箱填写错误");
            return 10000;
        }

        //提前添加乘机人
        PassengerCacheServices.startCache();

        //
        fireAv(tripConfig);

        return ConfigManager.getInstance().getSetting().qps;
    }


    private static void fireAv(final ConfigManager.TripBean tripConfig) {

        if (isOrder && System.currentTimeMillis() - orderStart < 20000) {
            //20s内只允许有一次提交
            return;
        }
        orderStart = 0;

        List<ConfigManager.PassengerBean> passengerList = ConfigManager.getInstance().getPassengerList();

        if (passengerList.isEmpty()) {
            ActivityHooker.updatePanel("请配置乘机人列表:");
            return;
        }

        tripConfig.dep = tripConfig.dep.toUpperCase();
        tripConfig.arr = tripConfig.arr.toUpperCase();

        PassengerNum passengerNum = computePassengerNum(passengerList);
        if (passengerNum.getAdultNum() <= 0) {
            ActivityHooker.updatePanel("该订单没有成人，请检查乘机人配置");
            return;
        }
        // ActivityHooker.updatePanel("");
        JSONObject requestJson = new JSONObject(true);
        requestJson.put("adults", String.valueOf(passengerNum.getAdultNum()));
        requestJson.put("children", String.valueOf(passengerNum.getChildNum()));
        requestJson.put("infantsInLap", "0");
        requestJson.put("infantsInSeat", "");
        requestJson.put("seniors", "");
        requestJson.put("foreAir", "open");
        requestJson.put("page", 1);
        requestJson.put("sliceIndex", 0);

        JSONObject depAndArr = new JSONObject(true);
        depAndArr.put("date", tripConfig.depDate);
        depAndArr.put("destination", tripConfig.arr);
        depAndArr.put("arrCityFlag", true);
        depAndArr.put("origin", tripConfig.dep);
        depAndArr.put("depCityFlag", true);
        JSONArray array = new JSONArray();
        array.add(depAndArr);
        requestJson.put("slices", array);

        NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/inter/querySingleWayPriceByQpxc.do", requestJson.toJSONString(), new NetworkServices.NetworkCallback() {
            @Override
            public void onSuccess(String body) {
                failedTimes = 0;
                JSONObject avResult = JSON.parseObject(body);

                JSONObject jsonObject = filterFlight(avResult, tripConfig.flightNumber);
                if (jsonObject == null) {

                    String message = avResult.getString("MESSAGE");
                    if (!TextUtils.isEmpty(message)) {
                        ActivityHooker.updatePanel(message + "  最后AV时间:" + DateTime.now().toString("yyyy-MM-dd HH:mm:ss"));
                        return;
                    }
                    ActivityHooker.updatePanel("没有发现航班:" + tripConfig.flightNumber + " 请确认配置");
                    return;
                }

                HashSet<String> sameCabins = new HashSet<>(Lists.newArrayList(tripConfig.cabins.split(",")));
                JSONObject filterCabinJson = filterCabin(jsonObject, sameCabins);
                if (filterCabinJson == null) {
                    ActivityHooker.updatePanel("没有满足条件的航班->没有仓位:" + StringUtils.join(sameCabins, ",") + "  最后AV时间:" + DateTime.now().toString("yyyy-MM-dd HH:mm:ss"));
                    return;
                }
                String bookingClassAvails = filterCabinJson.getString("bookingClassAvails");
                int seat = 0;
                if (StringUtils.contains(bookingClassAvails, ">9")) {
                    seat = 10;
                } else {
                    seat = Integer.parseInt(bookingClassAvails);
                }
                ActivityHooker.updatePanel("当前余座：" + seat + "  最后AV时间:" + DateTime.now().toString("yyyy-MM-dd HH:mm:ss"));
                if (seat >= ConfigManager.getInstance().getPassengerList().size() && !isOrder) {
                    //生单
                    WeChatNotifyService.sendWechatNotify("余票监控：\n" +
                            "乘机人:" + JSONObject.toJSONString(ConfigManager.getInstance().getPassengerList()) + "\n" +
                            "余票:" + seat
                    );
                    OrderLogger.outLog("avResult: " + body);
                    OrderLogger.outLog("发现余票：" + seat);
                    beginOrder(jsonObject, filterCabinJson, avResult.getString("id"));
                }
            }

            @Override
            public void onFiled(Exception e) {
                ActivityHooker.updatePanel("网络异常：" + e.getMessage());

                failedTimes++;
                FileLogger.outLog("当前异常次数:" + failedTimes);
                if (failedTimes > 3) {
                    int devices = 1;
                    ConfigManager.Setting setting = ConfigManager.getInstance().getSetting();
                    try {
                        devices = Integer.parseInt(setting.multiDevice);
                    } catch (Exception ignore) {
                        //
                    }
                    setting.multiDevice = String.valueOf(devices + 1);
                    FileLogger.outLog("递增设备id:" + setting.multiDevice);
                    ConfigManager.getInstance().updateSetting(setting);
                    RatelToolKit.processUtils.killMe();
                }
            }
        });
    }

    private static int failedTimes = 0;


    private static void beginOrder(JSONObject filterFlight, JSONObject filterCabinJson, String session) {
        isOrder = true;
        orderStart = System.currentTimeMillis();
        submitCabin(filterCabinJson, filterFlight, session);
    }

    private static void submitOrder(Double displayFareTotal, final Integer displayPrice, final JSONObject filterCabinJson, JSONObject filterFlight, String session,
                                    String solutionSet, String solution, String cabin
    ) {
        JSONObject jsonObject = new JSONObject(true);

        final JSONObject userInfo = Account.getLoginTempFile();
        if (userInfo == null) {
            ActivityHooker.updatePanel("当前设备退出登录");
            return;
        }

        List<JSONObject> submitPassenger = PassengerCacheServices.getSubmitPassenger();
        if (submitPassenger == null) {
            OrderLogger.outLog("乘机人添加失败");
            ActivityHooker.appendPanel("乘机人添加失败");
            WeChatNotifyService.sendWechatNotify("乘机人添加失败");
            return;
        }
        jsonObject.put("adultPrice", displayFareTotal);
        jsonObject.put("referralCode", "");
        jsonObject.put("enjoyFlag", false);
        jsonObject.put("passengers", buildPassenger(submitPassenger));
        JSONObject shelvesProduct = new JSONObject();
        shelvesProduct.put("productList", Lists.newArrayList());
        shelvesProduct.put("totalMoney", 0);
        jsonObject.put("shelvesProduct", shelvesProduct);
        jsonObject.put("ext", buildExt(session, solutionSet, solution));
        jsonObject.put("order", buildCreateOrderRequest(userInfo.getString("CARD_NO"),
                userInfo.getString("CN_NAME"), filterFlight, cabin, displayPrice, filterCabinJson));

        jsonObject.put("totalMoney", displayPrice);

        String orderParam = jsonObject.toJSONString();
        OrderLogger.outLog("生单参数:" + orderParam);
        //
        //NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/international/booking",
        NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/international/createGoOrder",
                orderParam, new NetworkServices.NetworkCallback() {
                    @Override
                    public void onSuccess(String body) {
                        if (TextUtils.isEmpty(body)) {
                            ActivityHooker.appendPanel("生单返回为空");
                            return;
                        }
                        OrderLogger.outLog("订单body: " + body);
                        FileLogger.outLog("订单body: " + body);
                        if (body.contains("创建订单失败")) {
                            ActivityHooker.appendPanel("创建订单失败");
                            return;
                        }

                        try {
                            JSONObject orderResponse = JSONObject.parseObject(body);

                            String orderno = orderResponse.getString("orderNo");
                            if (StringUtils.isBlank(orderno)) {
                                WeChatNotifyService.sendWechatNotify(
                                        "生单失败:\n" +
                                                body
                                );
                                ActivityHooker.appendPanel("生单失败:" + body);
                                return;
                            }

                            //附加账号内容
                            orderResponse.putAll(userInfo);
                            //删除无意义的
                            orderResponse.remove("Set-Cookie");
                            orderResponse.remove("QRCODEURL");
                            orderResponse.remove("APP_TOKEN_ID");
                            orderResponse.remove("LOGIN_TOKEN");
                            orderResponse.remove("OTHER_ID");
                            orderResponse.remove("OTHER_IDS");
                            orderResponse.remove("PASSPORT");
                            orderResponse.remove("PASSPORTS");

                            //附加订单价格
                            orderResponse.put("price", String.valueOf(displayPrice));
                            ActivityHooker.appendPanel("生单成功-订单号: " + body);

                            WeChatNotifyService.sendWechatNotify(
                                    "生单成功:\n" +
                                            "订单:" + orderResponse + "\n"
                                            + "账号:" + Account.userName + "\n"
                                            + "密码:" + Account.password + "\n"
                            );
                            running = false;
                            ConfigManager.TripBean tripConfig = ConfigManager.getInstance().getTripConfig();
                            tripConfig.ok = true;
                            ConfigManager.getInstance().updateTripBean(tripConfig);
                        } catch (JSONException e) {
                            ActivityHooker.appendPanel("订单返回解析失败:" + e.getMessage());
                        }
                    }

                    @Override
                    public void onFiled(Exception e) {
                        ActivityHooker.updatePanel("创建订单失败" + e.getMessage());
                        WeChatNotifyService.sendWechatNotify("创建订单失败" + e.getMessage());
                        //isOrder = false;
                    }
                });
    }


    private static List<JSONObject> buildPassenger(List<JSONObject> addPassengerRes) {
        List<JSONObject> params = Lists.newArrayList();

        for (JSONObject string : addPassengerRes) {
            JSONObject jsonObject = new JSONObject(true);
            jsonObject.put("birthdate", string.getString("birthdayDate"));
            jsonObject.put("email", "");
            String psgName = string.getString("psgName");
            String[] split = StringUtils.split(psgName, "\\/");
            jsonObject.put("firstName", split[1]);
            jsonObject.put("lastName", split[0]);

            jsonObject.put("fpCardNo", "");
            jsonObject.put("fpCompany", string.getString("fpCompany"));
            jsonObject.put("mobilePhone", "");
            jsonObject.put("nationality", string.getString("nationality"));
            jsonObject.put("psgId", string.getString("psgId"));
            jsonObject.put("insurance", "N");
            jsonObject.put("isEdm", 0);
            jsonObject.put("sex", string.getString("gender"));
            jsonObject.put("type", "00");
            jsonObject.put("carriedByPassengerId", "");

            JSONObject id = new JSONObject(true);
            id.put("countryOfIssue", string.getString("certIssueCountry"));
            id.put("number", string.getString("certNum"));
            id.put("type", string.getString("certType"));
            id.put("expiration", string.getString("certPeriodValidityDate"));
            jsonObject.put("identification", id);
            params.add(jsonObject);
        }
        return params;
    }


    private static JSONObject buildExt(String session, String solutionSet, String solution) {
        JSONObject jsonObject = new JSONObject(true);
        jsonObject.put("referer", session + "/" + solutionSet + "/" + solution);
        return jsonObject;
    }

    private static JSONObject buildCreateOrderRequest(
            String ffpCardno, String bookUserName, JSONObject filterFlight, String cabin,
            Integer displayPrice, JSONObject filterCabinJson) {
        JSONObject order = new JSONObject(true);

        order.put("docaFlag", false);
        order.put("products", buildProduct(filterFlight, cabin, filterCabinJson));
        order.put("usefoid", true);

        PassengerNum passengerNum = computePassengerNum(ConfigManager.getInstance().getPassengerList());
        order.put("adultNum", passengerNum.getAdultNum() + "");
        order.put("childNum", passengerNum.getChildNum() + "");
        order.put("infantNum", passengerNum.getInfantNum() + "");

        order.put("agreeAlternation", "NN");
        order.put("aid", "");
        order.put("attribute4", displayPrice + "");
        order.put("bookUser", ffpCardno);
        order.put("bookUserName", bookUserName);
        order.put("campaignScriptId", "12");
        order.put("contact", buildContact());
        order.put("domesticIndicate", "INTER");
        order.put("isEdm", 0);
        order.put("payBeforePnrFlag", false);
        order.put("seatNum", ConfigManager.getInstance().getPassengerList().size() + "");
        order.put("segType", "");
        order.put("vaildYhqUser", false);

        return order;
    }

    private static JSONObject buildContact() {
        JSONObject jsonObject = new JSONObject(true);

        ConfigManager.Contact contact = ConfigManager.getInstance().getContact();
        jsonObject.put("telephone", contact.phone);
        jsonObject.put("name", contact.name);
        jsonObject.put("mobile", contact.phone);
        jsonObject.put("email", StringUtils.isEmpty(contact.email) ? "" : contact.email);
        return jsonObject;
    }

    private static List<JSONObject> buildProduct(JSONObject filterFlight, String cabin, JSONObject filterCabinJson) {

        JSONObject avSegment = filterFlight.getJSONArray("segments").getJSONObject(0);
        JSONObject leg = avSegment.getJSONArray("legs").getJSONObject(0);

        JSONObject jsonObject = new JSONObject(true);
        jsonObject.put("taxtotal", filterFlight.getJSONArray("prices").getJSONObject(0).getIntValue("saleTaxTotal"));
        jsonObject.put("productType", "ITA");

        JSONObject segment = new JSONObject(true);
        JSONArray segments = new JSONArray();
        jsonObject.put("segments", segments);

        ConfigManager.TripBean tripConfig = ConfigManager.getInstance().getTripConfig();
        segments.add(segment);
        segment.put("arrAirport", tripConfig.arr);
        segment.put("arrCity", tripConfig.arr);
        segment.put("arrTime", DateTime.parse(leg.getString("arrTime")).toString("yyyy-MM-dd HH:mm:SS"));
        segment.put("cabin", cabin);
        segment.put("carrier", "CZ");
        segment.put("couponNo", 1);
        segment.put("depAirport", tripConfig.dep);
        segment.put("depCity", tripConfig.dep);
        segment.put("depTime", DateTime.parse(leg.getString("depTime")).toString("yyyy-MM-dd HH:mm:SS"));
        segment.put("depTimeUtc", leg.getString("depTimeZone"));
        segment.put("destinationTerminal", avSegment.getString("arrTerm"));
        segment.put("flightDate", avSegment.getString("depDate"));
        segment.put("flightNo", avSegment.getString("flightNo"));
        segment.put("isDirect", true);
        segment.put("planeType", avSegment.getString("plane"));
        segment.put("realSegOrder", 1);
        int intValue = filterFlight.getJSONArray("segments").getJSONObject(0).getIntValue("segOrder");
        segment.put("segOrder", intValue);
        segment.put("stopCity", "");
        segment.put("term", avSegment.getString("depTerm"));

        JSONObject tagInfoJsonObject = filterCabinJson.getJSONObject("tagInfo");
        if (tagInfoJsonObject != null) {
            // 3.9.6增加
            segment.put("segmentLable", tagInfoJsonObject.getString("brandCode"));
            JSONObject segmentLable = new JSONObject();

            JSONObject interest = tagInfoJsonObject.getJSONArray("interests").getJSONObject(0);
            segmentLable.putAll(interest);
            segmentLable.remove("adultTaxTag");
            segmentLable.remove("carrier");
            segmentLable.remove("flightNo");
            segment.put("segmentLableText", segmentLable.toJSONString());
        }


        return Lists.newArrayList(jsonObject);
    }


    private static void submitCabin(final JSONObject filterCabinJson, final JSONObject filterFlight, final String session) {
        final String cabin = filterCabinJson.getJSONArray("cabins").getJSONObject(0).getString("name");


        final String solutionSet = filterFlight.getString("solutionSet");
        final String solution = filterCabinJson.getString("solutionId");

        // 选择仓位
        JSONObject requestJson = new JSONObject(true);
        requestJson.put("session", session);
        requestJson.put("solution", solution);
        requestJson.put("solutionSet", solutionSet);

        //NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/inter/queryPricing.do",
        NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/inter/queryPricingQpxc.do",
                requestJson.toJSONString(), new NetworkServices.NetworkCallback() {
                    @Override
                    public void onSuccess(String body) {
                        if (body != null && body.contains("请重新预定")) {
                            ActivityHooker.updatePanel("仓位选择失败:" + body);
                            return;
                        }
                        Double displayFareTotal = filterCabinJson.getDouble("saleFareTotal");
                        Integer displayPrice = filterCabinJson.getIntValue("salePrice");

                        try {
                            JSONObject jsonObject = JSONObject.parseObject(body);
                            if (!TextUtils.isEmpty(jsonObject.getString("ERRORCODE"))) {
                                String message = jsonObject.getString("MESSAGE");
                                if (TextUtils.isEmpty(message)) {
                                    message = body;
                                }
                                isOrder = false;
                                ActivityHooker.updatePanel("选择仓位失败:" + message);
                                WeChatNotifyService.sendWechatNotify("选择仓位失败:" + message);
                                return;
                            }
                            submitOrder(displayFareTotal, displayPrice, filterCabinJson, filterFlight, session, solutionSet, solution, cabin);
                        } catch (JSONException e) {
                            FileLogger.outLog("error: " + FileLogger.getTrack(e));
                        }

                    }

                    @Override
                    public void onFiled(Exception e) {
                        isOrder = false;
                        ActivityHooker.updatePanel("选择仓位失败:" + e.getMessage());
                        WeChatNotifyService.sendWechatNotify("选择仓位失败:" + e.getMessage());
                    }
                });
    }


    public static JSONObject filterCabin(JSONObject filterFlight, HashSet<String> sameCabins) {
        JSONArray prices = filterFlight.getJSONArray("prices");
        for (int i = 0; i < prices.size(); i++) {
            JSONArray cabins = prices.getJSONObject(i).getJSONArray("cabins");
            for (int j = 0; j < cabins.size(); j++) {
                String name = cabins.getJSONObject(j).getString("name");
                if (sameCabins.contains(name)) {
                    return prices.getJSONObject(i);
                }
            }
        }
        return null;
    }

    public static JSONObject filterFlight(JSONObject jsonObject, String flightNum) {
        JSONArray dateFlights = jsonObject.getJSONArray("dateFlights");
        if (dateFlights == null) {
            return null;
        }
        for (int i = 0; i < dateFlights.size(); i++) {
            JSONArray segments = dateFlights.getJSONObject(i).getJSONArray("segments");
            for (int j = 0; j < segments.size(); j++) {
                String flightNo = segments.getJSONObject(j).getString("flightNo");
                if (StringUtils.containsIgnoreCase(flightNum, flightNo)) {
                    return dateFlights.getJSONObject(i);
                }
            }
        }
        return null;
    }

    private static PassengerNum computePassengerNum(List<ConfigManager.PassengerBean> passengerList) {
        int adultNum = 0;
        int childNum = 0;
        int infantNum = 0;

        for (ConfigManager.PassengerBean passenger : passengerList) {
            if (passenger.getIsChild()) {
                childNum++;
            } else {
                adultNum++;
            }
        }
        return new PassengerNum(adultNum, childNum, infantNum);
    }
}
