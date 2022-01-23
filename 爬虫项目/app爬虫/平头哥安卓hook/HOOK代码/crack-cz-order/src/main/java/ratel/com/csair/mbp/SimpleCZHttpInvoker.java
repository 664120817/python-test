package ratel.com.csair.mbp;

import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;

import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

import external.org.apache.commons.io.IOUtils;

public class SimpleCZHttpInvoker {
    public static String get(String url) {
        try {
            HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
            connection.setRequestMethod("GET");
            connection.connect();
            int responseCode = connection.getResponseCode();
            if (responseCode != HttpURLConnection.HTTP_OK) {
                connection.disconnect();
                return null;
            }
            try (InputStream inputStream = connection.getInputStream()) {
                return IOUtils.toString(inputStream, StandardCharsets.UTF_8);
            } finally {
                connection.disconnect();
            }
        } catch (Exception e) {
            Log.e(RatelToolKit.TAG, "error for url:" + url, e);
            return null;
        }
    }


}
