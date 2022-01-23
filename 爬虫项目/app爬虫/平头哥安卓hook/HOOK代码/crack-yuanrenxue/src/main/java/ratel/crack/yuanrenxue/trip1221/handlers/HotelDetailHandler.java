package ratel.crack.yuanrenxue.trip1221.handlers;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import ratel.crack.yuanrenxue.trip1221.RPC;


public class HotelDetailHandler implements ActionHandler {

    @AutoBind(require = true)
    private int hotelId;

    @AutoBind
    private String currency;

    @Override
    public String action() {
        return "hoteldetail";
    }

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {

        Object jHotelDetailRequest = RposedHelpers.newInstance(
                RposedHelpers.findClass("com.ctrip.ibu.hotel.business.request.java.JHotelDetailRequest", RatelToolKit.hostClassLoader)
                , "10320662412", hotelId
        );

        RPC.sendHotelBaseJavaRequest(jHotelDetailRequest, sekiroResponse, currency);
    }
}
