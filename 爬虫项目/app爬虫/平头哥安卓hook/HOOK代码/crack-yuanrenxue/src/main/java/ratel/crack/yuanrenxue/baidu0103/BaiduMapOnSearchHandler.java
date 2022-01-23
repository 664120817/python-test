package ratel.crack.yuanrenxue.baidu0103;

import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Map;

public class BaiduMapOnSearchHandler implements ActionHandler {
    public BaiduMapOnSearchHandler() {
    }

    @Override
    public String action() {
        return "BaiduMapOnSearch";
    }

    @AutoBind(require = true)
    private String keyWord;

    @AutoBind
    private int page;


    @Override
    public void handleRequest(SekiroRequest sekiroRequest, SekiroResponse sekiroResponse) {

        //com.baidu.mapframework.provider.search.controller.OneSearchWrapper
        final Object oneSearchWrapper = createOnSearchWrapper();
        final Object searchResponseCallback = createSearchResponseCallback(sekiroResponse);

        new Handler(Looper.getMainLooper())
                .post(new Runnable() {
                    @Override
                    public void run() {
                        int sentRequestId = (int) RposedHelpers.callStaticMethod(
                                RposedHelpers.findClass("com.baidu.mapframework.searchcontrol.SearchControl", RatelToolKit.hostClassLoader),
                                "searchRequest", oneSearchWrapper, searchResponseCallback
                        );
                        Log.i(BaiduMap0103.TAG, "sentRequestId: " + sentRequestId);
                    }
                });


    }

    private Object createSearchResponseCallback(final SekiroResponse sekiroResponse) {
        //com.baidu.mapframework.searchcontrol.SearchResponse

        //动态代理，
        Class<?> searchResponseClass = RposedHelpers.findClass("com.baidu.mapframework.searchcontrol.SearchResponse", RatelToolKit.hostClassLoader);
        return Proxy.newProxyInstance(searchResponseClass.getClassLoader(),
                new Class[]{searchResponseClass}, new InvocationHandler() {
                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        Log.i(BaiduMap0103.TAG, "callback method: " + method, new Throwable());
                        if (method.getDeclaringClass().equals(Object.class)) {
                            // Object. method
                            return method.invoke(this, args);
                        }
                        //onSearchComplete
                        //onSearchError
                        if (method.getName().equals("onSearchComplete")) {
                            //成功的
                            sekiroResponse.success(ForceFiledViewer.toView(args[0]));
                        } else if (method.getName().equals("onSearchError")) {
                            // 失败
                            int errorCode = (int) RposedHelpers.callMethod(args[0], "getErrorCode");
                            sekiroResponse.failed(-1, String.valueOf(errorCode));
                        }
                        return null;
                    }
                });
    }

    private Object createOnSearchWrapper() {

        Object mapBound = RposedHelpers.newInstance(
                RposedHelpers.findClass("com.baidu.platform.comapi.basestruct.MapBound", RatelToolKit.hostClassLoader),
                (int) 1.2964171E7, 4820356, (int) 1.2965566E7, 4823379
        );

        Object point = RposedHelpers.newInstance(
                RposedHelpers.findClass("com.baidu.platform.comapi.basestruct.Point", RatelToolKit.hostClassLoader),
                1.2964869E7D, 4821868D
        );

        Map<String, Object> extParam = new HashMap<>();
        extParam.put("da_src", "poiSearchPG.serhistory");
        extParam.put("sut", 0);
        extParam.put("sug_input", "");
        extParam.put("sug", 2);
        extParam.put("spos", 0);
        extParam.put("sl", 0);
        extParam.put("route_traffic", 1);

        return RposedHelpers.newInstance(
                RposedHelpers.findClass("com.baidu.mapframework.provider.search.controller.OneSearchWrapper", RatelToolKit.hostClassLoader),
                keyWord, "131", page, mapBound, 17, point, extParam
        );
    }
}
