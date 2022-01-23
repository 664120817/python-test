package ratel.crack.yuanrenxue.baidu1221;

import android.util.Log;

import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.inspect.ClassLoadMonitor;
import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;
import com.virjar.ratel.api.rposed.RposedHelpers;
import com.virjar.ratel.api.rposed.callbacks.RC_LoadPackage;
import com.virjar.sekiro.Constants;
import com.virjar.sekiro.api.SekiroClient;
import com.virjar.sekiro.log.SekiroLogger;

import java.util.UUID;

/**
 * Created by virjar on 2018/10/6.
 */

public class BaiduEntry {
    public static final String tag = "BD_HOOK";
    public static long nativePointer = 0;
    public static Object searcherImplObject = null;

    public static void entry(RC_LoadPackage.LoadPackageParam lpparam) {


        //com.baidu.baidumaps.common.network.NetworkListener.onReceive
        ClassLoadMonitor.addClassLoadMonitor("com.baidu.baidumaps.common.network.NetworkListener",
                new ClassLoadMonitor.OnClassLoader() {
                    @Override
                    public void onClassLoad(Class<?> clazz) {
                        RposedBridge.hookAllMethods(clazz, "onReceive", new RC_MethodHook() {
                            @Override
                            protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                                param.setResult(null);
                            }
                        });
                    }
                });
        if (lpparam.packageName.equals(lpparam.processName)) {
            SuperAppium.TAG = tag;
            SekiroLogger.tag = tag;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        Thread.sleep(8 * 1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    SekiroClient.start("sekiro.virjar.com", Constants.defaultNatServerPort, UUID.randomUUID().toString(), "yrx-baidu-rpc")
                            .registerHandler(new OneSearchAction());
                }
            }).start();

        }

        //com.baidu.platform.comapi.newsearch.SearcherImpl#getPBResultInternal
        ClassLoadMonitor.addClassLoadMonitor("com.baidu.platform.comapi.newsearch.SearcherImpl", new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {
                RposedHelpers.findAndHookMethod(clazz, "getPBResultInternal",
                        int.class,
                        int.class,
                        int.class,
                        new RC_MethodHook() {
                            @Override
                            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                                // 获取该对象，用于后续获取解析 protobuf 后的响应。
                                if (searcherImplObject == null) {
                                    searcherImplObject = param.thisObject;
                                }
                            }
                        });
            }
        });


        ClassLoadMonitor.addClassLoadMonitor("com.baidu.platform.comjni.map.searchengine.NASearchEngine", new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {

                RposedHelpers.findAndHookMethod(clazz, "nativeRequest",
                        long.class,
                        String.class,
                        new RC_MethodHook() {
                            @Override
                            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                                Log.d(tag, "nativeRequest nativePointer: " + param.args[0]);
                                if (nativePointer == 0) {
                                    nativePointer = (long) param.args[0];
                                }
                            }
                        });

            }
        });

        //com.baidu.mapframework.searchcontrol.SearchControl#searchRequest
        //com.baidu.mapframework.searchcontrol.SearchControl.searchRequest
//        ClassLoadMonitor.findAndHookMethod("com.baidu.mapframework.searchcontrol.SearchControl",
//                "searchRequest",
//                "com.baidu.mapframework.provider.search.controller.SearchWrapper",
//                "com.baidu.mapframework.searchcontrol.SearchResponse", new RC_MethodHook() {
//                    @Override
//                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
//                        Object searchWrapper = param.args[0];
//                        Log.i(tag, "search request , wrapper class: " + searchWrapper.getClass(), new Throwable());
//                        Log.i(tag, "body:" + JSON.toJSONString(ForceFiledViewer.toView(searchWrapper)));
//                    }
//                }
//        );

//        ClassLoadMonitor.addClassLoadMonitor("com.baidu.mapframework.searchcontrol.SearchControl", new ClassLoadMonitor.OnClassLoader() {
//            @Override
//            public void onClassLoad(Class<?> clazz) {
//                RposedHelpers.findAndHookMethod(clazz, "searchRequest", "com.baidu.mapframework.provider.search.controller.SearchWrapper",
//                        "com.baidu.mapframework.searchcontrol.SearchResponse", new RC_MethodHook() {
//                            @Override
//                            protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
//                                Object searchWrapper = param.args[0];
//                                Log.i(tag, "search request , wrapper class: " + searchWrapper.getClass(), new Throwable());
//                                //Log.i(tag, "body:" + JSON.toJSONString(ForceFiledViewer.toView(searchWrapper)));
//                            }
//                        });
//            }
//        });

        Log.i(tag, "hook end");
    }

    private static void backup() {


        //com.baidu.entity.pb.PoiResult
        ClassLoadMonitor.hookAllConstructor("com.baidu.entity.pb.PoiResult",
                new RC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        Log.i(tag, "new instance of PoiResult: ", new Throwable());
                    }
                });

        //com.baidu.mapframework.place.PoiItem
        ClassLoadMonitor.addClassLoadMonitor(new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {
                if (clazz.getName().startsWith("com.baidu.mapframework.place")) {
                    Log.i(tag, "init class: " + clazz);
                }
                if (clazz.getName().equals("com.baidu.mapframework.place.PoiItem")) {
                    RposedBridge.hookAllConstructors(clazz, new RC_MethodHook() {
                        @Override
                        protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                            Log.w(tag, "new instance: " + param.thisObject, new Throwable());
                        }
                    });
                }
                if (ClassLoadMonitor.tryLoadClass("com.baidu.mapframework.place.PoiItem")
                        .isAssignableFrom(clazz)
                ) {
                    RposedBridge.hookAllConstructors(clazz, new RC_MethodHook() {
                        @Override
                        protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                            Log.w(tag, "new instance: " + param.thisObject, new Throwable());
                        }
                    });
                }
            }
        });

//        RposedBridge.hookAllMethods(TextView.class, "setText", new RC_MethodHook() {
//            @Override
//            protected void afterHookedMethod(MethodHookParam param) throws Throwable {
//                if (param.args.length > 0 && param.args[0] instanceof CharSequence) {
//                    String textViewContent = param.args[0].toString();
//                    if (textViewContent.contains("加油站")) {
//                        Log.w(tag, "set value for :" + textViewContent, new Throwable());
//                    }
//                }
//            }
//        });


    }

}
