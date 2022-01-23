package ratel.crack.yuanrenxue.trip1221;

import android.text.TextUtils;

import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.Socket;

public class VirjarSocketFactory {
    public static Socket newSocket() {
        String property = System.getProperty("virjar-sockts-proxy");
        if (TextUtils.isEmpty(property)) {
            return new Socket();
        }
        String[] split = property.trim().split(":");
        InetSocketAddress inetSocketAddress = new InetSocketAddress(split[0].trim(), Integer.parseInt(split[1]));
        Proxy proxy = new Proxy(Proxy.Type.SOCKS, inetSocketAddress);
        return new Socket(proxy);
    }
}
