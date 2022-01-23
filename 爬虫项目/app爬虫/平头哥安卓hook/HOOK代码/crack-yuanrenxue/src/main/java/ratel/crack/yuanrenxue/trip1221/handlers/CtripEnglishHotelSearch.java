package ratel.crack.yuanrenxue.trip1221.handlers;

import android.annotation.SuppressLint;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.LinkedHashMap;

import ratel.crack.yuanrenxue.trip1221.RPC;


public class CtripEnglishHotelSearch implements ActionHandler {

    @AutoBind
    private String checkIn;

    @AutoBind(defaultIntValue = 1)
    private Integer pageNo;

//    @AutoBind(defaultStringValue = "1444")
//    private String priceMax;

    @AutoBind(require = true)
    private double latitude;

    @AutoBind(require = true)
    private double longitude;

    @AutoBind
    private String currency;

    @AutoBind(require = true)
    private String hotelId;

    @AutoBind(defaultIntValue = 1)
    private int roomCount;

    @AutoBind(defaultIntValue = 1)
    private int adultCount;

    @AutoBind(defaultIntValue = 1)
    private int childCount;

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {

        // com.ctrip.ibu.hotel.business.request.java.HotelSearchJavaRequest hotelSearchJavaRequest = new com.ctrip.ibu.hotel.business.request.java.HotelSearchJavaRequest(str);
        // 10320607445 酒店列表
        Object hotelSearchJavaRequest = RposedHelpers.newInstance(RposedHelpers.findClass("com.ctrip.ibu.hotel.business.request.java.HotelSearchJavaRequest", RatelToolKit.hostClassLoader), "10320607445");

        Date checkInDate = parse(checkIn);

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(checkInDate);
        calendar.add(Calendar.DAY_OF_YEAR, 1);
        Date end = calendar.getTime();

        RposedHelpers.callMethod(hotelSearchJavaRequest, "setDateRange", checkInDate, end);
        RposedHelpers.callMethod(hotelSearchJavaRequest, "setPage", pageNo, 10);

        RposedHelpers.callMethod(hotelSearchJavaRequest, "setPriceRange", "0", "-1");

        //入住人数和房间剩余数量,数组里面是 childAgeList，儿童需要安装年龄排序
        RposedHelpers.callMethod(hotelSearchJavaRequest, "setGuestAndRoom", adultCount, new ArrayList<>(), roomCount);

        RposedHelpers.callMethod(hotelSearchJavaRequest, "setSearchTags", createSearchTags());
        RposedHelpers.callMethod(hotelSearchJavaRequest, "setFilterConditions", createFilterConditions());

        RposedHelpers.callMethod(hotelSearchJavaRequest, "setRadius", 0D);

        RposedHelpers.callMethod(hotelSearchJavaRequest, "setCoordinateInfo", createCoordinateInfo());

        RposedHelpers.callMethod(hotelSearchJavaRequest, "setSearchConditions", createSearchConditions());

        //{"isAsc":false,"key":"key.hotel.sort.hotel.most.to.popular","value":38}
        RposedHelpers.callMethod(hotelSearchJavaRequest, "setSearchSort",
                RposedHelpers.getStaticObjectField(
                        RposedHelpers.findClass("com.ctrip.ibu.hotel.business.model.EHotelSort", RatelToolKit.hostClassLoader),
                        "MostPopular"
                )
        );

        RPC.sendHotelBaseJavaRequest(hotelSearchJavaRequest, sekiroResponse, currency);
    }

    private Object createCoordinateInfo() {
        Object jCoordinateInfo = RposedHelpers.newInstance(
                RposedHelpers.findClass("com.ctrip.ibu.hotel.business.response.java.hoteldetail.JCoordinateInfo", RatelToolKit.hostClassLoader)
        );

        RposedHelpers.callMethod(jCoordinateInfo, "setLatitude", latitude);
        RposedHelpers.callMethod(jCoordinateInfo, "setLongitude", longitude);
        return jCoordinateInfo;
    }


    private LinkedHashMap<String, String> createSearchConditions() {
        LinkedHashMap<String, String> searchConditions = new LinkedHashMap<>();
        //TODO 海外的话，设置成true
        searchConditions.put("ISOVERSEA", "F");
        searchConditions.put("CT", "1");
        searchConditions.put("H", hotelId);//hotelId
        searchConditions.put("AMOUNTSHOWTYPE", "0");
        return searchConditions;
    }


    private static LinkedHashMap<String, String> createFilterConditions() {
        LinkedHashMap<String, String> filterConditions = new LinkedHashMap<>();
        filterConditions.put("BOOKONLY", "F");
        filterConditions.put("INSTANTCONFIRMONLY", "F");
        filterConditions.put("BREAKFASTONLY", "F");
        filterConditions.put("FREECANCELONLY", "F");
        filterConditions.put("COUPONFILTER", "F");
        filterConditions.put("OPENBATCHSEARCH", "T");
        filterConditions.put("MEMBERPOINTS", "T");
        return filterConditions;
    }


    private static LinkedHashMap<String, String> createSearchTags() {

        LinkedHashMap<String, String> searchTags = new LinkedHashMap<>();
        searchTags.put("QUERYTYPE", "H");
        searchTags.put("BUSINESS", "F");
        searchTags.put("QUERYSOURCE", "NORMAL");
        searchTags.put("OPENSEQ", "T");
        searchTags.put("TRIPPLUSWEEK", "T");
        searchTags.put("OPENDIAMOND", "T");
        searchTags.put("COUPON_AFTER_PROMOTION", "T");
        searchTags.put("OPEN_NEW_USER_REWARD", "T");
        searchTags.put("CROSS_INCENTIVE", "T");
        searchTags.put("OPENFGTAX", "T");
        searchTags.put("COINS_TO_PAYMENT", "T");
        searchTags.put("ENABLE_ROOM_CHILD_POLICY", "T");
        searchTags.put("OPEN_HOUR_ROOM", "T");
        searchTags.put("OPEN_MELLOW_HOTEL", "T");
        searchTags.put("PRICE_DISPLAY_DECIMAL", "T");
        searchTags.put("OPEN_MEMBER_OPTIMIZE", "T");
        return searchTags;
    }

    public static Date parse(String text) {
        @SuppressLint("SimpleDateFormat") SimpleDateFormat dateFormatter = new SimpleDateFormat("yyyy-MM-dd");
        try {
            return dateFormatter.parse(text);
        } catch (ParseException e) {
            e.printStackTrace();
            throw new IllegalStateException("parse data failed: " + text + ": " + e.getMessage());
        }
    }

    @Override
    public String action() {
        return "hotelSearch";
    }
}
