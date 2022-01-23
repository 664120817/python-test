package ratel.crack.yuanrenxue.trip1221.handlers;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import ratel.crack.yuanrenxue.trip1221.RPC;


public class KeyWordSearchHandler implements ActionHandler {
    //search type
    public static final String DESTINATION = "D";
    public static final String KEYWORD = "K";
    public static final String NEARBY = "N";


    // search condition
    public static String BED = "BED";
    public static String BREAKFAST = "BREAKFAST";
    public static String D_PROVINCE = "D_PROVINCE";
    public static String FACILITY = "HF";
    public static String PAY = "PAY";
    public static String STAR = "STAR";


    @AutoBind(require = true)
    private String keyword;

    @AutoBind(require = true)
    private double latitude;

    @AutoBind(require = true)
    private double longitude;

    /**
     * 城市
     */
    @AutoBind(defaultIntValue = 274)
    private int code;

    @AutoBind
    private String currency;

    @Override
    public String action() {
        return "keywordsearch";
    }

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {
        Object hotelKeywordSearchRequest = RposedHelpers.newInstance(RposedHelpers.findClass("com.ctrip.ibu.hotel.business.request.java.HotelKeywordSearchRequest", RatelToolKit.hostClassLoader));

        //关键词搜索
        RposedHelpers.callMethod(hotelKeywordSearchRequest, "setSearchType", KEYWORD);
        RposedHelpers.callMethod(hotelKeywordSearchRequest, "setKeyword", keyword);

        RposedHelpers.callMethod(hotelKeywordSearchRequest,
                "setSearchConditions",
                (Object) new String[]{FACILITY, BED, PAY, BREAKFAST}
        );


        Object coordinateInfo = genCoordinateInfo();
        RposedHelpers.callMethod(hotelKeywordSearchRequest, "setCoordinateInfo", coordinateInfo);
        RposedHelpers.callMethod(hotelKeywordSearchRequest, "setCityCodeOfUser", 1);


        RposedHelpers.callMethod(hotelKeywordSearchRequest, "setCodeType", "CT");
        RposedHelpers.callMethod(hotelKeywordSearchRequest, "setCode", code);

        RPC.sendHotelBaseJavaRequest(hotelKeywordSearchRequest, sekiroResponse, currency);
    }

    private Object genCoordinateInfo() {
        Object coordinateInfo = RposedHelpers.newInstance(
                RposedHelpers.findClass("com.ctrip.ibu.hotel.business.request.java.HotelKeywordSearchRequest$CoordinateInfo", RatelToolKit.hostClassLoader)
        );
        RposedHelpers.callMethod(coordinateInfo, "setCoordinateType", "GD");
        RposedHelpers.callMethod(coordinateInfo, "setLatitude", latitude);
        RposedHelpers.callMethod(coordinateInfo, "setLongitude", longitude);
        return coordinateInfo;
    }
}
