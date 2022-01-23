package ratel.crack.yuanrenxue.trip1221.handlers;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

import ratel.crack.yuanrenxue.trip1221.RPC;


public class RatelPlanHandler implements ActionHandler {
    @Override
    public String action() {
        return "ratePlan";
    }

    @AutoBind
    private String checkIn;

    @AutoBind
    private String checkOut;

    @AutoBind(require = true)
    private int hotelId;

    /**
     * 来自 group=ctrip-english&action=hotelSearch&checkIn=2020-10-21&latitude=39.76984&longitude=106.585989&hotelId=1990801
     */
    @AutoBind(require = true)
    private String hotelUniqueKey;

    @AutoBind(defaultIntValue = 1)
    private int roomCount;

    @AutoBind(defaultIntValue = 1)
    private int adultCount;

    @AutoBind(defaultIntValue = 1)
    private int childCount;

    @AutoBind
    private String currency;


    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {

        Object jHotelRatePlanRequest = RposedHelpers.newInstance(RposedHelpers.findClass("com.ctrip.ibu.hotel.business.request.java.JHotelRatePlanRequest", RatelToolKit.hostClassLoader), "10320662412");

        RposedHelpers.callMethod(jHotelRatePlanRequest, "setDateRange",
                CtripEnglishHotelSearch.parse(checkIn), CtripEnglishHotelSearch.parse(checkOut)
        );

        RposedHelpers.callMethod(jHotelRatePlanRequest, "setHotelCode", hotelId);
        RposedHelpers.callMethod(jHotelRatePlanRequest, "setHotelUniqueKey", hotelUniqueKey);

        RposedHelpers.callMethod(jHotelRatePlanRequest, "setRoomCount", roomCount);

        //com.ctrip.ibu.hotel.business.model.GuestCount

        Object guestCount = RposedHelpers.newInstance(
                RposedHelpers.findClass("com.ctrip.ibu.hotel.business.model.GuestCount", RatelToolKit.hostClassLoader)
        );
        RposedHelpers.callMethod(guestCount, "setAdult", adultCount);
        RposedHelpers.callMethod(guestCount, "setChild", new ArrayList<>());
        RposedHelpers.callMethod(jHotelRatePlanRequest, "setGuestCount", guestCount);

        addSearchTags(jHotelRatePlanRequest);
        addFilterConditions(jHotelRatePlanRequest);
        addSearchConditions(jHotelRatePlanRequest);

        RPC.sendHotelBaseJavaRequest(jHotelRatePlanRequest, sekiroResponse, currency);
    }


    private void addSearchConditions(Object jHotelRatePlanRequest) {
        LinkedHashMap<String, String> searchConditions = new LinkedHashMap<>();
        searchConditions.put("AMOUNTSHOWTYPE", "0");
        for (Map.Entry<String, String> item : searchConditions.entrySet()) {
            RposedHelpers.callMethod(jHotelRatePlanRequest, "addSearchCondition", item.getKey(), Integer.valueOf(item.getValue()));
        }
    }


    private static void addFilterConditions(Object jHotelRatePlanRequest) {
        LinkedHashMap<String, String> filterConditions = new LinkedHashMap<>();
        filterConditions.put("COUPONFILTER", "T");
        filterConditions.put("NEEDALL", "T");
        filterConditions.put("MEMBERPOINTS", "T");

        for (Map.Entry<String, String> item : filterConditions.entrySet()) {
            RposedHelpers.callMethod(jHotelRatePlanRequest, "addFilterCondition", item.getKey(), item.getValue());
        }
    }


    private static void addSearchTags(Object jHotelRatePlanRequest) {

        LinkedHashMap<String, String> searchTags = new LinkedHashMap<>();
        searchTags.put("BUSINESS", "F");
        searchTags.put("TRIPPLUSWEEK", "T");
        searchTags.put("OPENDIAMOND", "T");
        searchTags.put("COUPON_AFTER_PROMOTION", "T");
        searchTags.put("OPEN_CANCEL_FLOAT_LAYER", "T");
        searchTags.put("COINS_TO_PAYMENT", "T");
        searchTags.put("ENABLE_ROOM_CHILD_POLICY", "T");
        searchTags.put("TOP_COINS_SCRIPT", "T");
        searchTags.put("MEAL_INFO_NEW_OPEN", "T");
        searchTags.put("OPEN_HOUR_ROOM", "T");
        searchTags.put("OPEN_MELLOW_HOTEL", "T");
        searchTags.put("OPEN_MEMBER_OPTIMIZE", "T");
        searchTags.put("PRICE_DISPLAY_DECIMAL", "T");
        searchTags.put("OPEN_JUSTIFYCONFIRM_CONTENT", "T");
        searchTags.put("OPEN_NEW_USER_REWARD", "T");
        searchTags.put("METAROOM", "T");
        searchTags.put("OPENFGTAX", "T");

        for (Map.Entry<String, String> item : searchTags.entrySet()) {
            RposedHelpers.callMethod(jHotelRatePlanRequest, "addSearchTag", item.getKey(), item.getValue());
        }
    }
}
