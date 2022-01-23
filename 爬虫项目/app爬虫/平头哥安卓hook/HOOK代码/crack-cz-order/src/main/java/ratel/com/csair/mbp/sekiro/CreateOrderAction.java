package ratel.com.csair.mbp.sekiro;

import android.text.TextUtils;

import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.inspect.Lists;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import org.joda.time.DateTime;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

import external.com.alibaba.fastjson.JSON;
import external.com.alibaba.fastjson.JSONArray;
import external.com.alibaba.fastjson.JSONException;
import external.com.alibaba.fastjson.JSONObject;
import external.com.alibaba.fastjson.serializer.SerializerFeature;
import external.org.apache.commons.lang3.StringUtils;
import ratel.com.csair.mbp.Account;
import ratel.com.csair.mbp.beans.Contactor;
import ratel.com.csair.mbp.beans.FlightQuery;
import ratel.com.csair.mbp.beans.Passenger;
import ratel.com.csair.mbp.beans.PassengerAdaptor;
import ratel.com.csair.mbp.beans.PassengerModel;
import ratel.com.csair.mbp.beans.PassengerNum;
import ratel.com.csair.mbp.services.NetworkServices;

public class CreateOrderAction implements ActionHandler {

    @Override
    public String action() {
        return "createOrder";
    }

    @AutoBind
    private JSONObject filterFlight;

    @AutoBind
    private String sameCabins;


    @AutoBind(require = true)
    private Contactor contactor;

    @AutoBind(require = true)
    private FlightQuery flightQuery;

    @AutoBind(require = true)
    private JSONArray passengers;


    private List<Passenger> passengerList;

    // 订单提交需要的参数
    private List<JSONObject> addedPassengerList = new ArrayList<>();

    private Double displayFareTotal;
    private Integer displayPrice;

    private String session;
    private String solutionSet;
    private String solution;
    private String cabin;

    private JSONObject userInfo;
    private final Object avLock = new Object();
    private final Object passengerLock = new Object();
    private boolean avReady = false;
    private boolean psgReady = false;


    private SekiroResponse mSekiroResponse;
    private boolean isFailed = false;

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {
        userInfo = Account.getLoginTempFile();
        FileLogger
                .outLog("接受生单请求: avContent: " + filterFlight + "  orderParam: " + JSONObject.toJSONString(flightQuery));
        if (userInfo == null) {
            FileLogger.outLog("当前用户为登录");
            sekiroResponse.failed("user not login");
            return;
        }

        passengerList = Lists.newArrayListWithCapacity(passengers.size());
        for (int i = 0; i < passengers.size(); i++) {
            JSONObject passenger = passengers.getJSONObject(i);
            passengerList.add(passenger.toJavaObject(Passenger.class));
        }

        mSekiroResponse = sekiroResponse;
        //乘机人添加，或者查询，结果放到addedPassengerList中
        operatePassenger(userInfo);
        // 过滤仓位，选择指定仓位
        operateAv();

        if (!avReady) {
            synchronized (avLock) {
                try {
                    avLock.wait(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }

        if (!psgReady) {
            synchronized (passengerLock) {
                try {
                    passengerLock.wait(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
        if (!isFailed) {
//            FileLogger.outLog("开始order");
            order();
        }
    }


    private void failed(String message) {
        isFailed = true;
        synchronized (avLock) {
            avLock.notifyAll();
        }
        synchronized (passengerLock) {
            passengerLock.notifyAll();
        }

        FileLogger.outLog("失败信息: " + message);
        mSekiroResponse.failed(message);
    }

    private void order() {
        JSONObject jsonObject = new JSONObject(true);

        jsonObject.put("adultPrice", displayFareTotal);
        jsonObject.put("referralCode", "");
        jsonObject.put("enjoyFlag", false);
        jsonObject.put("passengers", buildPassenger(addedPassengerList));
        jsonObject.put("ext", buildExt(session, solutionSet, solution));
        jsonObject.put("order", buildCreateOrderRequest(contactor, passengerList, userInfo.getString("CARD_NO"),
                userInfo.getString("CN_NAME"), filterFlight, flightQuery, cabin, displayPrice));

//        FileLogger.outLog("圣诞参数: " + jsonObject.toJSONString());

        NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/international/booking",
                jsonObject.toJSONString(), new NetworkServices.NetworkCallback() {
                    @Override
                    public void onSuccess(String body) {
                        if (TextUtils.isEmpty(body)) {
                            failed("生单返回空");
                            return;
                        }
                        FileLogger.outLog("订单body: " + body);
                        if (body.contains("创建订单失败")) {
                            failed(body);
                        }

                        try {
                            JSONObject orderResponse = JSONObject.parseObject(body);
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
                            mSekiroResponse.success(orderResponse);
                        } catch (JSONException e) {
                            failed(body);
                        }
                    }

                    @Override
                    public void onFiled(Exception e) {
                        failed("预定失败: " + FileLogger.getTrack(e));
                    }
                });

    }

    private List<JSONObject> buildPassenger(List<JSONObject> addPassengerRes) {
        List<JSONObject> params = Lists.newArrayList();

        for (JSONObject string : addPassengerRes) {
//            FileLogger.outLog("构造乘机人参数: " + string);
            JSONObject passenger;
            //if (queryPassengerList.size() != 0) {
            passenger = string;

//            } else {
//                passenger = string.getJSONObject("vo");
//            }

            JSONObject jsonObject = new JSONObject(true);
            jsonObject.put("birthdate", passenger.getString("birthdayDate"));
            jsonObject.put("email", "");
            String psgName = passenger.getString("psgName");
            String[] split = StringUtils.split(psgName, "\\/");
            jsonObject.put("firstName", split[1]);
            jsonObject.put("lastName", split[0]);

            jsonObject.put("fpCardNo", "");
            jsonObject.put("fpCompany", passenger.getString("fpCompany"));
            jsonObject.put("mobilePhone", "");
            jsonObject.put("nationality", passenger.getString("nationality"));
            jsonObject.put("psgId", passenger.getString("psgId"));
            jsonObject.put("insurance", "N");
            jsonObject.put("isEdm", 0);
            jsonObject.put("sex", passenger.getString("gender"));
            jsonObject.put("type", "00");

            JSONObject id = new JSONObject(true);
            id.put("countryOfIssue", passenger.getString("certIssueCountry"));
            id.put("number", passenger.getString("certNum"));
            id.put("type", passenger.getString("certType"));
            id.put("expiration", passenger.getString("certPeriodValidityDate"));
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

    private static JSONObject buildCreateOrderRequest(Contactor contactor, List<Passenger> passengerList,
                                                      String ffpCardno, String bookUserName, JSONObject filterFlight, FlightQuery flightQuery, String cabin,
                                                      Integer displayPrice) {
        JSONObject order = new JSONObject(true);

        order.put("docaFlag", false);
        order.put("products", buildProduct(filterFlight, flightQuery, cabin));
        order.put("usefoid", true);

        PassengerNum passengerNum = computePassengerNum(passengerList);
        order.put("adultNum", passengerNum.getAdultNum() + "");
        order.put("childNum", passengerNum.getChildNum() + "");
        order.put("infantNum", passengerNum.getInfantNum() + "");

        order.put("agreeAlternation", "NN");
        order.put("aid", "");
        order.put("attribute4", displayPrice + "");
        order.put("bookUser", ffpCardno);
        order.put("bookUserName", bookUserName);
        order.put("campaignScriptId", "12");
        order.put("contact", buildContact(contactor));
        order.put("domesticIndicate", "INTER");
        order.put("isEdm", 0);
        order.put("payBeforePnrFlag", false);
        order.put("seatNum", passengerList.size() + "");
        order.put("segType", "");
        order.put("vaildYhqUser", false);

        return order;
    }

    private static JSONObject buildContact(Contactor contact) {
        JSONObject jsonObject = new JSONObject(true);

        jsonObject.put("telephone", contact.getPhoneNumber());
        jsonObject.put("name", contact.getFullName());
        jsonObject.put("mobile", contact.getPhoneNumber());
        jsonObject.put("email", StringUtils.isEmpty(contact.getEmail()) ? "" : contact.getEmail());
        return jsonObject;
    }

    private static List<JSONObject> buildProduct(JSONObject filterFlight, FlightQuery flightQuery, String cabin) {

        JSONObject avSegment = filterFlight.getJSONArray("segments").getJSONObject(0);
        JSONObject leg = avSegment.getJSONArray("legs").getJSONObject(0);

        JSONObject jsonObject = new JSONObject(true);
        jsonObject.put("taxtotal", filterFlight.getJSONArray("prices").getJSONObject(0).getIntValue("saleTaxTotal"));
        jsonObject.put("productType", "ITA");

        JSONObject segment = new JSONObject(true);
        JSONArray segments = new JSONArray();
        jsonObject.put("segments", segments);

        segments.add(segment);
        segment.put("arrAirport", flightQuery.getArrAirportCode());
        segment.put("arrCity", flightQuery.getArrCityNameZH());
        segment.put("arrTime", DateTime.parse(leg.getString("arrTime")).toString("yyyy-MM-dd HH:mm:SS"));
        segment.put("cabin", cabin);
        segment.put("carrier", "CZ");
        segment.put("couponNo", 1);
        segment.put("depAirport", flightQuery.getDepAirportCode());
        segment.put("depCity", flightQuery.getDepCityNameZH());
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

        return Lists.newArrayList(jsonObject);
    }

    private void operateAv() {
        HashSet<String> sameCabinSet = new HashSet<>();
        if (!TextUtils.isEmpty(sameCabins)) {
            sameCabinSet.addAll(Lists.newArrayList(sameCabins.split(",")));
        }
        final JSONObject filterCabinJson = filterCabin(filterFlight, sameCabinSet);
        if (filterCabinJson == null) {
            FileLogger.outLog("没找到对应仓位{}", JSON.toJSONString(sameCabins));
            failed("没找到对应仓位:" + sameCabins);
            return;
        }
        cabin = filterCabinJson.getJSONArray("cabins").getJSONObject(0).getString("name");

        session = filterFlight.getString("session");
        solutionSet = filterFlight.getString("solutionSet");
        solution = filterCabinJson.getString("solutionId");

        // 选择仓位
        JSONObject requestJson = new JSONObject(true);
        requestJson.put("session", session);
        requestJson.put("solution", solution);
        requestJson.put("solutionSet", solutionSet);
        NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/inter/queryPricing.do",
                requestJson.toJSONString(), new NetworkServices.NetworkCallback() {
                    @Override
                    public void onSuccess(String body) {
                        if (body != null && body.contains("请重新预定")) {
                            failed("仓位选择失败:" + body);
                            return;
                        }
                        displayFareTotal = filterCabinJson.getDouble("saleFareTotal");
                        displayPrice = filterCabinJson.getIntValue("salePrice");

                        try {
                            JSONObject jsonObject = JSONObject.parseObject(body);
                            if (!TextUtils.isEmpty(jsonObject.getString("ERRORCODE"))) {
                                String message = jsonObject.getString("MESSAGE");
                                if (TextUtils.isEmpty(message)) {
                                    message = body;
                                }
                                failed(message);
                                return;
                            }
                        } catch (JSONException e) {
                            FileLogger.outLog("error: " + FileLogger.getTrack(e));
                        }

                        FileLogger.outLog("仓位操作完成..");
                        synchronized (avLock) {
                            avReady = true;
                            avLock.notifyAll();
                        }
                    }

                    @Override
                    public void onFiled(Exception e) {
                        FileLogger.outLog("仓位选择失败:" + FileLogger.getTrack(e));
                        failed("仓位选择失败:" + FileLogger.getTrack(e));
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

    private void operatePassenger(final JSONObject userInfo) {

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

                        for (Passenger passenger : passengerList) {
                            if (existedPassengerMap.containsKey(passenger.getCardNum().toUpperCase())) {
                                addedPassengerList.add(existedPassengerMap.get(passenger.getCardNum().toUpperCase()));
                                // FileLogger.outLog("添加乘机人结果:" + addedPassengerList);
                                FileLogger.outLog("乘机人已经存在，不需要添加:" + JSONObject.toJSONString(passenger));
                            } else {
                                addPassenger(passenger, userInfo.getString("CARD_NO"));
                            }
                        }
                        if (addedPassengerList.size() == passengerList.size()) {
                            FileLogger.outLog("所有乘机人都已经添加到账号中，直接触发生单...");
                            synchronized (passengerLock) {
                                psgReady = true;
                                passengerLock.notifyAll();
                            }
                        }
                    }

                    @Override
                    public void onFiled(Exception e) {
                        failed("乘机人查询失败:" + FileLogger.getTrack(e));
                    }
                }
        );
    }


    private void addPassenger(final Passenger passenger, String ffpCardno) {
        PassengerModel passengerModel = new PassengerModel(
                passenger.getBirthday(),
                passenger.getCardIssuePlace(),
                passenger.getCardNum(),
                passenger.getPassportExpireDate(),
                PassengerAdaptor.getIdType(passenger.getCardType()),
                PassengerAdaptor.getSexType(passenger.getGender()),
                passenger.getPassengerType() == PassengerAdaptor.PASSENGER_TYPE_ADULT,
                passenger.getCardIssuePlace(),
                passenger.getLastName() + "/" + passenger.getFirstName(),
                ffpCardno);

        NetworkServices.sendPostRequest("https://3g.csair.com/CSMBP/bookProcess/order/account/modifyPassengerInfo",
                JSON.toJSONString(passengerModel, SerializerFeature.WriteMapNullValue),
                new NetworkServices.NetworkCallback() {
                    @Override
                    public void onSuccess(String body) {
                        addedPassengerList.add(JSONObject.parseObject(body).getJSONObject("vo"));
                        if (addedPassengerList.size() == passengerList.size()) {
                            synchronized (passengerLock) {
                                psgReady = true;
                                passengerLock.notifyAll();
                            }
                        }
                    }

                    @Override
                    public void onFiled(Exception e) {
                        FileLogger
                                .outLog("添加乘机人失败:" + JSONObject.toJSONString(passenger) + " stack: " + FileLogger.getTrack(e));
                        failed("添加乘机人失败:" + JSONObject.toJSONString(passenger) + " stack: " + FileLogger.getTrack(e));
                    }
                }
        );
    }

    private static PassengerNum computePassengerNum(List<Passenger> passengerList) {
        int adultNum = 0;
        int childNum = 0;
        int infantNum = 0;
        for (Passenger passenger : passengerList) {
            if (PassengerAdaptor.PASSENGER_TYPE_ADULT == passenger.getPassengerType()) {
                adultNum++;
            } else if (PassengerAdaptor.PASSENGER_TYPE_CHILD == passenger.getPassengerType()) {
                childNum++;
            } else if (PassengerAdaptor.PASSENGER_TYPE_INFANT == passenger.getPassengerType()) {
                infantNum++;
            }
        }
        return new PassengerNum(adultNum, childNum, infantNum);
    }

}
