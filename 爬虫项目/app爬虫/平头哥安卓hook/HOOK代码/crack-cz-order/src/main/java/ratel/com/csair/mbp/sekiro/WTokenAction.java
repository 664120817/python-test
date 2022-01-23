package ratel.com.csair.mbp.sekiro;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import org.apache.commons.codec.DecoderException;
import org.apache.commons.codec.binary.Hex;

public class WTokenAction implements ActionHandler {
    @Override
    public String action() {
        return "wToken";
    }

    @AutoBind
    private String hexParam;

    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {

        Class<?> wTokenClass = RposedHelpers.findClass("com.csair.mbp.netrequest.net.a", RatelToolKit.hostClassLoader);
        Object wTokenBytes = null;
        try {
            wTokenBytes = Hex.decodeHex(hexParam.toCharArray());
        } catch (DecoderException e) {
            sekiroResponse.failed(e.getMessage());
            return;
        }
        String wToken = (String) RposedHelpers.callStaticMethod(wTokenClass, "a", wTokenBytes);//加密字节数组
        sekiroResponse.success(wToken);
    }
}
