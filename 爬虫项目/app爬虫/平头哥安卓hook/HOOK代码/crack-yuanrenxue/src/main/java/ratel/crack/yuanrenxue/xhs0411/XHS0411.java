package ratel.crack.yuanrenxue.xhs0411;

import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.Constants;
import com.virjar.sekiro.api.ActionHandler;
import com.virjar.sekiro.api.SekiroClient;
import com.virjar.sekiro.api.SekiroRequest;
import com.virjar.sekiro.api.SekiroResponse;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.net.URL;
import java.util.UUID;

import external.com.alibaba.fastjson.JSON;

public class XHS0411 {
    private static final String tag = "XHS_HOOK";

    // https://down.52pojie.cn/Tools/Android_Tools/

    public static void entry(final RC_LoadPackage.LoadPackageParam lpparam) {
        if (!lpparam.packageName.equals(lpparam.processName)) {
            return;
        }
        RposedBridge.hookAllConstructors(URL.class, new RC_MethodHook() {
            @Override
            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                URL url = (URL) param.thisObject;
                // https://edith.xiaohongshu.com/api/sns/v6/homefeed?oid=homefeed_recommend&cursor_score=&geo=eyJsYXRpdHVkZSI6MC4wMDAwMDAsImxvbmdpdHVkZSI6MC4wMDAwMDB9%0A&trace_id=a5425829-5827-3408-940e-1b34821f29ad&note_index=0&refresh_type=1&client_volume=0.60&preview_ad=&loaded_ad=%7B%22ads_id_list%22%3A%5B%5D%7D&personalization=1&pin_note_id=&pin_note_source=&unread_begin_note_id=604ac3010000000001029dd2&unread_end_note_id=6072c48a000000002103785b&unread_note_count=4
                if (url.toString().contains("api/sns/v6/homefeed")) {
                    // kotlin, okhttp3，rxJava
                    // okhttp3 + Retrofit + rxJava

                    // Retrofit2 ->  sns/v6/homefeed

                    Log.i(tag, "access url : " + url, new Throwable());
                }
            }
        });


        //com.xingin.matrix.explorefeed.model.ExploreService.queryHomeFeed(
        // java.lang.String,  oid              -> homefeed_recommend
        // java.lang.String,  cursor_score     -> ""
        // java.lang.String,  geo              -> eyJsYXRpdHVkZSI6MC4wMDAwMDAsImxvbmdpdHVkZSI6MC4wMDAwMDB9\n
        // java.lang.String,  trace_id         -> tring v14 = h.b(); uuid//

        // int,               note_index       -> 0
        // int,               refresh_type     -> PASSIVE_REFRESH
        // java.lang.String,  client_volume    -> AudioManager v8_1 = (AudioManager)v8; float v0 = ((float)v8_1.getStreamVolume(3)) / ((float)v8_1.getStreamMaxVolume(3)); String.format("%.2f",xxx)
        // java.lang.String,  preview_ad       -> ""

        // java.lang.String,  loaded_ad        -> {\"ads_id_list\":[\"5093429\"]}
        // int,               personalization  ->   e.b().a("config_personalization", 1);
        // java.lang.String,  pin_note_id           -> ""
        // java.lang.String,  pin_note_source       -> ""

        // java.lang.String,  unread_begin_note_id  -> ""
        // java.lang.String,  unread_end_note_id    -> ""
        // int                unread_note_count     -> 0
        // ) : s.a.r


        // n.d0.j0.l.g.d.a.a(java.lang.String, java.lang.String, java.lang.String,              int,  n.d0.j0.l.a.a,   java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, java.lang.String, int              ) : s.a.r
        RposedBridge.hookAllMethods(
                RposedHelpers.findClass("n.d0.j0.l.g.d.a", lpparam.classLoader),
                "a",
                new RC_MethodHook() {
                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "queryHomeFeed : args: " + JSON.toJSONString(param.args) + " result:" + param.getResult().getClass());
                        Log.i(tag, "queryHomeFeed stack trace:", new Throwable());
                    }
                }
        );

        SekiroClient.start("sekiro.virjar.com", Constants.defaultNatServerPort,
                UUID.randomUUID().toString(), "pdd0302")
                .registerHandler(new ActionHandler() {
                    @Override
                    public String action() {
                        return "homefeed";
                    }

                    @Override
                    public void handleRequest(SekiroRequest sekiroRequest, final SekiroResponse sekiroResponse) {

                        // (ExploreService)b.c.a(ExploreService.class);

                        Class<?> retrofitApiManagerClass = RposedHelpers.findClass("n.d0.m0.b.b", lpparam.classLoader);
                        Object retrofitApiManager = RposedHelpers.getStaticObjectField(retrofitApiManagerClass, "c");

                        Class<?> exploreServiceClass = RposedHelpers.findClass("com.xingin.matrix.explorefeed.model.ExploreService", lpparam.classLoader);


                        Object exploreService = RposedHelpers.callMethod(retrofitApiManager, "a", exploreServiceClass);

                        //n.d0.j0.l.j.h
                        Class<?> hClass = RposedHelpers.findClass("n.d0.j0.l.j.h", lpparam.classLoader);
                        String traceId = (String) RposedHelpers.callStaticMethod(hClass, "b");


                        // int v20 = e.b().a("config_personalization", 1);
                        Class<?> eClass = RposedHelpers.findClass("n.d0.y1.y0.e", lpparam.classLoader);
                        Object e = RposedHelpers.callStaticMethod(eClass, "b");
                        Integer personalization = (Integer) RposedHelpers.callMethod(e, "a", "config_personalization", 1);

                        Object rxJavaObservable = RposedHelpers.callMethod(exploreService, "queryHomeFeed",
                                "homefeed_recommend", "", "eyJsYXRpdHVkZSI6MC4wMDAwMDAsImxvbmdpdHVkZSI6MC4wMDAwMDB9\n", traceId,

                                0, 3, "30.44", "",

                                "{\"ads_id_list\":[\"5093429\"]}", personalization, "", "",

                                "", "", 0
                        );

                        // task
                        // javascript Promise 许诺，允诺
                        // java Future   未来
                        // rxJava Observable

                        final Class<?> ObserverClass = RposedHelpers.findClass("s.a.x", lpparam.classLoader);
                        Object observer = Proxy.newProxyInstance(ObserverClass.getClassLoader(), new Class[]{ObserverClass}, new InvocationHandler() {
                            @Override
                            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                                if (method.getDeclaringClass() != ObserverClass) {
                                    //object hashCode,toString
                                    return method.invoke(this, args);
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

//                        Class<?> rxrObserverClass = RposedHelpers.findClass("s.a.yrx.YRXObserver", lpparam.classLoader);
//                        Object observer = RposedHelpers.newInstance(rxrObserverClass, sekiroResponse);

                        //observable.subscribe(observer);
                        RposedHelpers.callMethod(rxJavaObservable, "b", observer);

                        // method inline hook
                    }
                })
        ;
    }

    static {
        Class<?> rxrObserverClass = RposedHelpers.findClass("s.a.yrx.YRXObserver", RatelToolKit.hostClassLoader);
        RposedHelpers.findAndHookMethod(rxrObserverClass, "onError", Throwable.class, new RC_MethodHook() {
            @Override
            protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                Throwable throwable = (Throwable) param.args[0];
                Log.i(tag, "error", throwable);
                SekiroResponse sekiroResponse = RposedHelpers.getObjectField(param.thisObject, "addtion");
                sekiroResponse.failed(-1, throwable);
            }
        });

        RposedHelpers.findAndHookMethod(rxrObserverClass, "onNext", Object.class, new RC_MethodHook() {
            @Override
            protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                Object bean = param.args[0];
                SekiroResponse sekiroResponse = RposedHelpers.getObjectField(param.thisObject, "addtion");
                sekiroResponse.success(bean);
            }
        });
    }
}
