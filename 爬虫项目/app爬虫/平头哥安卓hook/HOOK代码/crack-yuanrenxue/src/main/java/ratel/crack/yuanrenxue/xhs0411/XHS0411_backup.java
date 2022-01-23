package ratel.crack.yuanrenxue.xhs0411;

import android.content.Intent;
import android.os.Parcel;
import android.util.Log;

import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.inspect.ForceFiledViewer;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.Constants;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroClient;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;
import com.virjar.sekiro.log.SekiroLogger;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.net.URL;
import java.util.UUID;

import external.com.alibaba.fastjson.JSONObject;

public class XHS0411_backup {
    private static final String tag = "XHS_HOOK";

    public static void entry(final RC_LoadPackage.LoadPackageParam lpparam) {

        if (!lpparam.packageName.equals(lpparam.processName)) {
            return;
        }

        SekiroLogger.tag = tag;
        SuperAppium.TAG = tag;

        RposedBridge.hookAllConstructors(URL.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(tag, "new URL: " + param.thisObject);
                if (param.thisObject.toString().contains("api/sns/v6/homefeed")) {
                    Log.i(tag, "homefeed query", new Throwable());
                }
            }
        });

        // com.xingin.matrix.explorefeed.refactor.SmoothExploreFragment$m.a(com.xingin.matrix.explorefeed.entities.FeedCategoriesBean) : s.a.r
        // com.xingin.matrix.explorefeed.refactor.SmoothExploreFragment$p.a(com.xingin.matrix.explorefeed.entities.FeedCategoriesBean) : s.a.r

        RC_MethodHook homeFeedMonitor = new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                Log.i(tag, "call " + param.method + " rClass:" + param.getResult().getClass(), new Throwable());
            }
        };

        RposedHelpers.findAndHookMethod("com.xingin.matrix.explorefeed.refactor.SmoothExploreFragment$m", lpparam.classLoader,
                "a",
                "com.xingin.matrix.explorefeed.entities.FeedCategoriesBean", homeFeedMonitor);

        RposedHelpers.findAndHookMethod("com.xingin.matrix.explorefeed.refactor.SmoothExploreFragment$p", lpparam.classLoader,
                "a",
                "com.xingin.matrix.explorefeed.entities.FeedCategoriesBean", homeFeedMonitor);


        SekiroClient.start("sekiro.virjar.com", Constants.defaultNatServerPort,
                UUID.randomUUID().toString(), "pdd0302")
                .registerHandler(new ActionHandler() {
                    @Override
                    public String action() {
                        return "getCategories";
                    }

                    @Override
                    public void handleRequest(SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {
                        // ((ExploreService)b.c.a(ExploreService.class)).getCategories();
                        Class<?> bClass = RposedHelpers.findClass("n.d0.m0.b.b", lpparam.classLoader);
                        Object apiService = RposedHelpers.getStaticObjectField(bClass, "c");

                        Class<?> exploreServiceClass = RposedHelpers.findClass("com.xingin.matrix.explorefeed.model.ExploreService", lpparam.classLoader);

                        Object exploreServiceApi = RposedHelpers.callMethod(apiService, "a", exploreServiceClass);

                        Object rxJavaObject = RposedHelpers.callMethod(exploreServiceApi, "getCategories");

                        final Class<?> observerClass = RposedHelpers.findClass("s.a.x", lpparam.classLoader);

                        Object observerOrConsumer = Proxy.newProxyInstance(rxJavaObject.getClass().getClassLoader(), new Class[]{observerClass},
                                new InvocationHandler() {
                                    @Override
                                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                                        if (method.getDeclaringClass() != observerClass) {
                                            return method.invoke(this, args);
                                        }
                                        if (args == null) {
                                            return null;
                                        }
                                        if (method.getName().equals("onNext")) {
                                            sekiroResponse.success(args[0]);
                                            return null;
                                        }
                                        if (method.getName().equals("onError")) {
                                            Throwable throwable = (Throwable) args[0];
                                            Log.i(tag, "error", throwable);
                                            sekiroResponse.failed(-1, throwable);
                                            return null;
                                        }
                                        return null;
                                    }
                                });

                        RposedHelpers.callMethod(rxJavaObject, "b", observerOrConsumer);

                    }
                });
    }

    private static void backup() {
        RposedHelpers.findAndHookMethod(Intent.class, "writeToParcel", Parcel.class, int.class,
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Intent intent = (Intent) param.thisObject;
                        intent.getStringExtra("test");
                        String sss = JSONObject.toJSONString(ForceFiledViewer.toView(intent));
                        loge("Result", sss);
                        Log.i(tag, "intent writeToParcel: " + sss);
                        Log.i(tag, "intent writeToParcel trace:", new Throwable());
                    }
                });
    }

    public static void loge(String tag, String msg) {
        if (tag == null || tag.length() == 0 || msg == null || msg.length() == 0) {
            return;
        }
        int segmentSize = 3 * 1024;
        long length = msg.length();
        if (length <= segmentSize) {// 长度小于等于限制直接打印
            Log.e(tag, msg);
        } else {
            while (msg.length() > segmentSize) {// 循环分段打印日志
                String logContent = msg.substring(0, segmentSize);
                msg = msg.replace(logContent, "");
                Log.i(tag, logContent);
            }
            Log.i(tag, msg);// 打印剩余日志
        }

    }
}
