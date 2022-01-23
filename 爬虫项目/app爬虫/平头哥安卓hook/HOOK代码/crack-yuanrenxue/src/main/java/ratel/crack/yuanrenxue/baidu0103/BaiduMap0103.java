package ratel.crack.yuanrenxue.baidu0103;

import android.text.TextUtils;
import android.util.Log;
import android.widget.TextView;

import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.api.SekiroClient;
import com.virjar.sekiro.log.SekiroLogger;

import java.util.Map;
import java.util.UUID;

import external.com.alibaba.fastjson.JSONObject;

public class BaiduMap0103 {
    public static final String TAG = "BD_HOOK";

    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {

        //com.baidu.mapframework.provider.search.controller.OneSearchWrapper#OneSearchWrapper(
        // java.lang.String, java.lang.String, int,
        // com.baidu.platform.comapi.basestruct.MapBound, int,
        // com.baidu.platform.comapi.basestruct.Point, java.util.Map<java.lang.String,java.lang.Object>)
        RposedHelpers.findAndHookConstructor(
                RposedHelpers.findClass("com.baidu.mapframework.provider.search.controller.OneSearchWrapper", lpparam.classLoader),
                String.class, String.class, int.class,
                "com.baidu.platform.comapi.basestruct.MapBound", int.class,
                "com.baidu.platform.comapi.basestruct.Point", Map.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "OneSearchWrapper: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args)));
                        Log.i(TAG, "OneSearchWrapper: " + JSONObject.toJSONString(param.thisObject));
                    }
                }
        );
        //com.baidu.platform.comjni.tools.ProtobufUtils#getMessageLite(java.lang.String, byte[], int, int)
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("com.baidu.platform.comjni.tools.ProtobufUtils", lpparam.classLoader),
                "getMessageLite", new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "getMessageLite :" + JSONObject.toJSONString(ForceFiledViewer.toView(param.getResult())));
                        Log.i(TAG, "stack trace:", new Throwable());
                    }
                }
        );

        //com.baidu.mapframework.searchcontrol.baseline.SearchBaseLineImpl#onResponse
        RposedHelpers.findAndHookMethod(
                "com.baidu.mapframework.searchcontrol.baseline.SearchBaseLineImpl", lpparam.classLoader,
                "onResponse",
                "com.baidu.platform.comapi.newsearch.result.AbstractSearchResult",
                java.util.Map.class, int.class, String.class, new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "onResponse:" + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[0])), new Throwable());
                    }
                }

        );


        //com.baidu.mapframework.searchcontrol.baseline.SearchOnline#response
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("com.baidu.mapframework.searchcontrol.baseline.SearchOnline", lpparam.classLoader),
                "response", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "SearchOnline -> response :", new Throwable());

                        Log.i(TAG, "requestMap :" + JSONObject.toJSONString(ForceFiledViewer.toView(
                                RposedHelpers.getObjectField(param.thisObject, "requestMap")
                        )));
                        Log.i(TAG, "requestId: " + RposedHelpers.callMethod(param.args[0], "getRequestId"));
                    }
                }
        );

        startSekiro(lpparam);
        Log.i(TAG, "hook end");
    }

    private static void startSekiro(RC_LoadPackage.LoadPackageParam lpparam) {
        if (!lpparam.packageName.equals(lpparam.processName)) {
            return;
        }
        SekiroLogger.tag = TAG;
        SuperAppium.TAG = TAG;
        SekiroClient.start("sekiro.virjar.com",
                UUID.randomUUID().toString(),
                "baidu0103")
                .registerHandler(new BaiduMapOnSearchHandler());
    }

    private static void backup(RC_LoadPackage.LoadPackageParam lpparam) {

        //com.baidu.platform.comapi.newsearch.NewSearchNotifier.dispatchResult(SourceFile:165)
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("com.baidu.platform.comapi.newsearch.NewSearchNotifier", lpparam.classLoader),
                "dispatchResult", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "NewSearchNotifier -> dispatchResult :", new Throwable());

                    }
                }
        );


        // com.baidu.mapframework.searchcontrol.baseline.SearchBaseLineDispatcher.dispatchResponse
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("com.baidu.mapframework.searchcontrol.baseline.SearchBaseLineDispatcher", lpparam.classLoader),
                "dispatchResponse", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "SearchBaseLineDispatcher -> dispatchResponse :", new Throwable());

                    }
                }
        );

        // hook pojo 构造 （网络响应反序列化）
        //com.baidu.entity.pb.PoiResult
        RposedBridge.hookAllConstructors(
                RposedHelpers.findClass("com.baidu.entity.pb.PoiResult", lpparam.classLoader),
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "create PoiResult: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.thisObject)),
                                new Throwable());
                    }
                }
        );

        // hook网络发出
        //com.baidu.platform.comapi.newsearch.SearcherImpl#sendRequest
        RposedHelpers.findAndHookMethod(
                "com.baidu.platform.comapi.newsearch.SearcherImpl", lpparam.classLoader,
                "sendRequest",
                "com.baidu.platform.comapi.newsearch.SearchRequest", new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                        Log.i(TAG, "sendRequest: " + JSONObject.toJSONString(ForceFiledViewer.toView(param.args[0])), new Throwable());
                    }
                }
        );

        // hook pojo 构造 （网络响应反序列化）
        //com.baidu.platform.comjni.tools.ProtobufUtils#getMessageLite(java.lang.String, byte[], int, int)
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("com.baidu.platform.comjni.tools.ProtobufUtils", lpparam.classLoader),
                "getMessageLite", new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(TAG, "getMessageLite :" + JSONObject.toJSONString(ForceFiledViewer.toView(param.getResult())));
                    }
                }
        );


        //寻找pojo
        RposedBridge.hookAllMethods(TextView.class, "setText",
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        String textContent = null;
                        for (Object obj : param.args) {
                            if (obj instanceof CharSequence) {
                                textContent = obj.toString();
                                break;
                            }
                        }
                        if (!TextUtils.isEmpty(textContent)) {
                            //Log.i(TAG, "setText for textView:" + textContent);
                            if (textContent.contains("亚朵酒店")) {
                                Log.i(TAG, "hint content:" + textContent, new Throwable());
                            }
                        }
                    }
                }
        );
    }

}
