package ratel.com.csair.mbp.services;

import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.FileLogger;
import com.virjar.ratel.api.inspect.ClassLoadMonitor;
import com.virjar.ratel.api.rposed.RposedHelpers;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;

import ratel.com.csair.mbp.HookEntry;

public class NetworkServices {


    public static boolean isReady() {
        return requestServicesClass != null && callbackHandlerClass != null;
    }


    private static Class<?> requestServicesClass = null;
    private static Class<?> callbackHandlerClass = null;

    static {
        ClassLoadMonitor.addClassLoadMonitor("com.csair.mbp.netrequest.net.okhttp.d", new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {
                requestServicesClass = clazz;
            }
        }, true);

        ClassLoadMonitor.addClassLoadMonitor("com.csair.mbp.netrequest.net.okhttp.b.b", new ClassLoadMonitor.OnClassLoader() {
            @Override
            public void onClassLoad(Class<?> clazz) {
                callbackHandlerClass = clazz;
            }
        }, true);
    }


    public static void sendPostRequest(String url, String body, final NetworkCallback networkCallback) {
        FileLogger.outLog("发送请求-> url: " + url + " body:" + body);
        if (requestServicesClass == null || callbackHandlerClass == null) {
            networkCallback.onFiled(new IllegalStateException("requestServicesClass not init"));
            return;
        }
        Object proxy;
        try {
            Method[] declaredMethods = callbackHandlerClass.getDeclaredMethods();
            List<Method> methods = new ArrayList<>();
            for (Method method : declaredMethods) {
                if (Modifier.isAbstract(method.getModifiers())) {
                    methods.add(method);
                }
            }
            proxy = RatelToolKit.dexMakerProxyBuilderHelper
                    .forClass(callbackHandlerClass)
                    .parentClassLoader(callbackHandlerClass.getClassLoader())
                    .onlyMethods(methods.toArray(new Method[]{}))
                    .handler(new InvocationHandler() {
                        @Override
                        public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                            Class<?>[] parameterTypes = method.getParameterTypes();
                            if (parameterTypes.length == 2 && parameterTypes[0].getName().equalsIgnoreCase("okhttp3.Response")) {
                                // public byte[] b(okhttp3.Response response, int i) throws java.io.IOException {
                                Object responseBody = RposedHelpers.callMethod(args[0], "body");
                                if (responseBody == null) {
                                    networkCallback.onFiled(new IllegalStateException("empty response"));
                                    return null;
                                }
                                String str;
                                try {
                                    str = (String) RposedHelpers.callMethod(responseBody, "string");
                                    FileLogger.outLog("请求结果：" + str);
                                } catch (Error e) {
                                    //Caused by: java.io.EOFException
                                    Log.e(HookEntry.TAG, "error", e);
                                    FileLogger.outLog("解析请求结果失败:" + e);
                                    networkCallback.onFiled(new Exception(e));
                                    return null;
                                }
                                networkCallback.onSuccess(str);
                                return null;
                            } else if (parameterTypes.length == 3
                                    && parameterTypes[1].getName().equalsIgnoreCase("java.lang.Exception")) {

                                // public abstract void a(okhttp3.Call call, java.lang.Exception exc, int i);
                                Exception exception = (Exception) args[1];
                                FileLogger.outLog("抓取异常:" + FileLogger.getTrack(exception));

                                networkCallback.onFiled(exception);
                                return null;
                            } else if (Modifier.isAbstract(method.getModifiers())) {
                                return null;
                            } else if (method.getDeclaringClass().equals(Object.class)) {
                                return method.invoke(this, args);
                            }
                            return method.invoke(this, args);
                        }
                    }).build();
        } catch (Throwable e) {
            FileLogger.outLog(FileLogger.getTrack(e));

            return;
        }

        try {
            RposedHelpers.callStaticMethod(requestServicesClass, "a", url, body, 60000, proxy);
        } catch (Throwable e) {
            FileLogger.outLog(FileLogger.getTrack(e));
        }
    }

    public static interface NetworkCallback {
        public void onSuccess(String body);

        public void onFiled(Exception e);
    }
}
