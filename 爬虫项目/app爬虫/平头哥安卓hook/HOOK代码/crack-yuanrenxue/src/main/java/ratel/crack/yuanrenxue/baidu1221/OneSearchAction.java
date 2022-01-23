package ratel.crack.yuanrenxue.baidu1221;

import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.inspect.ClassLoadMonitor;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.api.databind.AutoBind;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import external.com.alibaba.fastjson.JSONObject;
import external.org.apache.commons.lang3.tuple.Pair;

import static com.virjar.ratel.api.rposed.RposedHelpers.callMethod;
import static com.virjar.ratel.api.rposed.RposedHelpers.callStaticMethod;

public class OneSearchAction implements ActionHandler {

    @AutoBind(defaultStringValue = "https://newclient.map.baidu.com/client/phpui2/")
    String domain;

    @AutoBind(defaultStringValue = "0")
    String sug;

    // 地图缩放等级
    @AutoBind(defaultStringValue = "17")
    String level;

    // 搜索关键词
    @AutoBind(defaultStringValue = "美食")
    String word;

    // 城市 id
    @AutoBind(defaultStringValue = "131")
    String cityId;

    // 第几页数据
    @AutoBind(defaultStringValue = "0")
    String pageNum;

    // 一页返回多少条数据
    @AutoBind(defaultStringValue = "10")
    String resultNum;

    @AutoBind(defaultStringValue = "1")
    String requestType;

    @AutoBind(defaultStringValue = "20")
    String busResultNum;

    @AutoBind(defaultStringValue = "32")
    String extInfo;

    // 搜索目标经度
    @AutoBind(require = true)
    String lng;

    // 搜索目标纬度
    @AutoBind(require = true)
    String lat;

    // 搜索起始经度（用于计算当前到目标的距离）
    @AutoBind(defaultStringValue = "116.521285")
    String startLng;

    // 搜索起始纬度（用于计算当前到目标的距离）
    @AutoBind(defaultStringValue = "39.917025")
    String startLat;

    ExecutorService cachedThreadPool = Executors.newCachedThreadPool();

    @Override
    public String action() {
        return "BDSearch";
    }


    @Override
    public void handleRequest(SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {

        if (BaiduEntry.nativePointer == 0 || BaiduEntry.searcherImplObject == null) {
            sekiroResponse.failed("应用未初始化完成，请稍后再试！");
            new Handler(Looper.getMainLooper()).post(new Runnable() {
                @Override
                public void run() {

                    RatelToolKit.processUtils.killMe();

                }
            });
            return;
        }


        // 利用百度地图自己的方式生成 seid
        // com.baidu.platform.comapi.util.MD5
        Class<?> MD5Class = ClassLoadMonitor.tryLoadClass("com.baidu.platform.comapi.util.MD5");
        //com.baidu.platform.comapi.util.SysOSAPIv2
        Class<?> SysOSAPIv2Class = ClassLoadMonitor.tryLoadClass("com.baidu.platform.comapi.util.SysOSAPIv2");
        Object SysOSAPIv2 = RposedHelpers.callStaticMethod(SysOSAPIv2Class, "getInstance");
        String cuid = (String) RposedHelpers.callMethod(SysOSAPIv2, "getCuid");
        Log.d(BaiduEntry.tag, "handleRequest cuid: " + cuid);

        String seid = (String) RposedHelpers.callStaticMethod(MD5Class, "getMD5String", cuid + System.currentTimeMillis());
        Log.d(BaiduEntry.tag, "handleRequest seid: " + seid);

        JSONObject ldataJsonObject = new JSONObject();
        ldataJsonObject.put("src_from", "mainpg_search");
        ldataJsonObject.put("se_id", seid);

        // wd 生成
        // com.baidu.platform.comapi.util.URLEncodeUtils
        Class<?> URLEncodeUtilsClass = ClassLoadMonitor.tryLoadClass("com.baidu.platform.comapi.util.URLEncodeUtils");
        String wd = (String) RposedHelpers.callStaticMethod(URLEncodeUtilsClass, "urlEncode", word);
        Log.d(BaiduEntry.tag, "handleRequest wd: " + wd);
        Pair<Double, Double> locPair = getbd09mcPair(Double.parseDouble(lng), Double.parseDouble(lat));

        // 左下角及右上角坐标
        Pair<Pair<Double, Double>, Pair<Double, Double>> pair = Util.getQueryScope(locPair.getLeft(), locPair.getRight(), Integer.parseInt(level));
        String b = String.format("(%s,%s;%s,%s)", pair.getLeft().getLeft(), pair.getLeft().getRight(), pair.getRight().getLeft(), pair.getRight().getRight()).trim();
        Log.d(BaiduEntry.tag, "b: " + b);

        // 中心坐标
        String loc = String.format("(%s,%s)", locPair.getLeft(), locPair.getRight());
        Log.d(BaiduEntry.tag, "loc: " + loc);

        Pair<Double, Double> startPair = getbd09mcPair(Double.parseDouble(startLng), Double.parseDouble(startLat));
        String startLoc = String.format("%s,%s", startPair.getLeft(), startPair.getRight());
        Log.d(BaiduEntry.tag, "startLoc: " + startLoc);

        // com.baidu.platform.comapi.newsearch.params.poi.OneSearchParams#formJsonData
        JSONObject uriParamJsonObject = new JSONObject();
        uriParamJsonObject.put("qt", "s"); // 硬编码
        uriParamJsonObject.put("ie", "utf-8"); // 硬编码
        uriParamJsonObject.put("sug", sug); // USER(0)　SERVER(1), LOCAL(2); 默认为 0
        uriParamJsonObject.put("l", level); // level 默认为 17
        uriParamJsonObject.put("wd", wd); // WIFI_DISPLAY URLEncodeUtils.urlEncode(this.word)
        uriParamJsonObject.put("c", cityId); //cityId
        uriParamJsonObject.put("pn", pageNum); // pageNum
        uriParamJsonObject.put("rn", resultNum); //resultNum
        uriParamJsonObject.put("route_traffic", "1"); // routeTraffic 硬编码
        uriParamJsonObject.put("req", requestType); // requestType
        uriParamJsonObject.put("lrn", busResultNum); // busResultNum
        uriParamJsonObject.put("extinfo", extInfo); // extInfo
        uriParamJsonObject.put("sgeo_control", "1"); // 硬编码
        uriParamJsonObject.put("b", b);
        uriParamJsonObject.put("lasttype", "0");
        uriParamJsonObject.put("startloc", startLoc); // 起始地址
        uriParamJsonObject.put("sceneinfo", "");
        uriParamJsonObject.put("da_src", "poiSearchPG.searchBt");
        uriParamJsonObject.put("rp_filter", "simplified");
        uriParamJsonObject.put("version", "5");
        uriParamJsonObject.put("sug_input", word);
        uriParamJsonObject.put("startcity", cityId);
        uriParamJsonObject.put("biz", "poi_small_panel");
        uriParamJsonObject.put("ads_version", "2.2.2");
        uriParamJsonObject.put("ldata", ldataJsonObject.toJSONString());
        uriParamJsonObject.put("sl", "3");
        uriParamJsonObject.put("sub_version", "10241");
        uriParamJsonObject.put("loc", loc);
        uriParamJsonObject.put("rp_format", "pb");

        JSONObject monitorParamJsonObject = new JSONObject();
        monitorParamJsonObject.put("action", 201);

        JSONObject extParamJsonObject = new JSONObject();
        extParamJsonObject.put("data_format", "pb");
        extParamJsonObject.put("b_cache", true);
        extParamJsonObject.put("method", "post");
        extParamJsonObject.put("businessid", 20);
        extParamJsonObject.put("type", 11);
        extParamJsonObject.put("b_user_param", true);
        extParamJsonObject.put("b_sign", true);
        extParamJsonObject.put("b_signnew", true);
        extParamJsonObject.put("b_encode", true);
        extParamJsonObject.put("b_mmproxy", false);

        JSONObject paramJsonObject = new JSONObject();
        paramJsonObject.put("domain", domain);
        paramJsonObject.put("uri_param", uriParamJsonObject);
        paramJsonObject.put("monitor_param", monitorParamJsonObject);
        paramJsonObject.put("ext_param", extParamJsonObject);


        final Class<?> NASearchEngine = ClassLoadMonitor.tryLoadClass("com.baidu.platform.comjni.map.searchengine.NASearchEngine");
        String param = paramJsonObject.toJSONString();
        Log.d(BaiduEntry.tag, "Search param: " + param);

        // 发送搜索请求
        final int requestId = (int) callStaticMethod(NASearchEngine, "nativeRequest", BaiduEntry.nativePointer, param);
        Log.d(BaiduEntry.tag, "Search requestId: " + requestId);

        // 百度地图属于在 so 中进行异步处理请求，此处延迟 3 秒之后查询响应结果
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(3 * 1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                Object abstractSearchResult = callMethod(BaiduEntry.searcherImplObject, "getPBResultInternal", requestId, 1, 1);
                Log.d(BaiduEntry.tag, "Search result: " + ForceFiledViewer.toView(abstractSearchResult));
                sekiroResponse.success(ForceFiledViewer.toView(abstractSearchResult));
            }
        };
        cachedThreadPool.execute(runnable);


    }

    /**
     * @param lng 百度坐标系经度
     * @param lat 百度坐标系纬度
     * @return 百度墨卡托坐标
     */
    private Pair<Double, Double> getbd09mcPair(Double lng, Double lat) {
        // com.baidu.platform.comapi.location.CoordinateUtil
        // 百度地图并不直接使用经纬度，而是使用墨卡托坐标需要进行转换
        // 经纬度可能有偏差，此处默认给出的经纬度采用的是百度的坐标系， 即 bd09ll。
        // 如果请求不是用百度坐标系获取的经纬度，会有有小量偏差。
        // 经纬度转变为墨卡托坐标 http://lbsyun.baidu.com/index.php?title=FAQ/iOS/loc
        Class<?> CoordinateUtilClass = ClassLoadMonitor.tryLoadClass("com.baidu.platform.comapi.location.CoordinateUtil");
        Object point = RposedHelpers.callStaticMethod(CoordinateUtilClass, "bd09llTobd09mc", lng, lat);
        Double x = (Double) RposedHelpers.callMethod(point, "getDoubleX");
        Double y = (Double) RposedHelpers.callMethod(point, "getDoubleY");
        Log.d(BaiduEntry.tag, "handleRequest point: x =  " + x + " y = " + y);
        return Pair.of(x, y);
    }


}
