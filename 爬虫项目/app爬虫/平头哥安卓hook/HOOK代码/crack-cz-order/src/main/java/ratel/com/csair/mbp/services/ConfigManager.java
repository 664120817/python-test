package ratel.com.csair.mbp.services;

import android.text.TextUtils;

import com.virjar.ratel.api.extension.FileLogger;

import org.joda.time.DateTime;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import ratel.com.csair.mbp.utils.FileUtils;

public class ConfigManager {
    public JSONObject config = null;
    public static ConfigManager instance = new ConfigManager();

    private ConfigManager() {
        load();
    }


    public static ConfigManager getInstance() {
        return instance;
    }

    public static class Account {
        public String account;
        public String password;
    }

    public List<Account> getAccountList() {
        JSONArray accounts = config.optJSONArray("accounts");
        List<Account> ret = new ArrayList<>();
        if (accounts == null) {
            JSONArray jsonArray = new JSONArray();
            try {
                config.put("accounts", jsonArray);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return ret;
        }


        for (int i = 0; i < accounts.length(); i++) {
            JSONObject jsonObject = accounts.optJSONObject(i);
            String account = jsonObject.optString("account");
            String pwd = jsonObject.optString("password");
            Account account1 = new Account();
            account1.account = account;
            account1.password = pwd;
            ret.add(account1);
        }
        return ret;
    }

    public void removeAccount(String userName) {
        if (TextUtils.isEmpty(userName)) {
            return;
        }
        userName = userName.trim();
        JSONArray accountList = config.optJSONArray("accounts");
        if (accountList == null) {
            return;
        }
        for (int i = accountList.length() - 1; i >= 0; i--) {
            JSONObject jsonObject = accountList.optJSONObject(i);
            String account = jsonObject.optString("account");
            if (userName.equals(account)) {
                accountList.remove(i);
                save();
            }
        }
    }

    public void addAccount(String userName, String password) {
        if (TextUtils.isEmpty(userName) ||
                TextUtils.isEmpty(password)
        ) {
            return;
        }
        userName = userName.trim();
        password = password.trim();
        JSONArray accountList = config.optJSONArray("accounts");
        if (accountList == null) {
            return;
        }
        for (int i = accountList.length() - 1; i >= 0; i--) {
            JSONObject jsonObject = accountList.optJSONObject(i);
            String account = jsonObject.optString("account");
            if (userName.equals(account)) {
                try {
                    jsonObject.putOpt("password", password);
                    return;
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }
        JSONObject newItem = new JSONObject();
        try {
            newItem.put("account", userName);
            newItem.put("password", password);
            accountList.put(newItem);
            save();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private void save() {
        File file = new File("/storage/emulated/0/ratel_white_dir/com.csair.mbp/order_task.json");


        if (file.exists() && !file.canWrite()) {

            return;
        }
        try {
            File parentFile = file.getParentFile();
            if (!parentFile.exists()) {
                parentFile.mkdirs();
            }
            String s = config.toString();

            FileOutputStream fileOutputStream = new FileOutputStream(file);
            fileOutputStream.write(s.getBytes(StandardCharsets.UTF_8));
            fileOutputStream.close();

            FileUtils.writeToFile(s.getBytes(StandardCharsets.UTF_8), new File("/sdcard/ratel_white_dir/com.csair.mbp/order_task.json"));
        } catch (IOException e) {

            FileLogger.outLog("error: " + FileLogger.getTrack(e));
            e.printStackTrace();
        }
    }

    private void load() {

        File file = new File("/sdcard/ratel_white_dir/com.csair.mbp/order_task.json");
        if (!file.exists() || !file.canRead()) {
            config = new JSONObject();
            return;
        }

        byte[] bytes = FileUtils.readFile(file);


        try {
            config = new JSONObject(new String(bytes, StandardCharsets.UTF_8));
        } catch (Exception e) {
            file.delete();
            throw new RuntimeException(e);
        }
    }


    public static class TripBean {
        public String dep = "";
        public String arr = "";
        public String flightNumber = "";
        public String depDate = "";
        public String cabins = "Y";
        public boolean ok = false;
    }

    public TripBean getTripConfig() {
        JSONObject trip = config.optJSONObject("trip");
        TripBean tripBean = new TripBean();
        if (trip == null) {
            return tripBean;
        }
        tripBean.dep = trip.optString("dep");
        tripBean.arr = trip.optString("arr");
        tripBean.flightNumber = trip.optString("flightNumber");
        tripBean.depDate = trip.optString("depDate");
        tripBean.cabins = trip.optString("cabins");
        tripBean.ok = trip.optBoolean("ok", false);
        return tripBean;
    }

    public void updateTripBean(TripBean tripBean) {
        JSONObject trip = config.optJSONObject("trip");
        if (trip == null) {
            trip = new JSONObject();
            try {
                config.put("trip", trip);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        try {
            trip.put("dep", tripBean.dep);
            trip.put("arr", tripBean.arr);
            trip.put("flightNumber", tripBean.flightNumber);
            trip.put("depDate", tripBean.depDate);
            trip.put("cabins", tripBean.cabins);
            trip.put("ok", tripBean.ok);
            save();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public static class PassengerBean {
        public String userName;
        public String gender;
        public String birthday;
        public String certNumber;
        public String certType;
        public String certExpireDate;
        public String cardIssuePlace;

        private Boolean isChild = null;

        public Boolean getIsChild() {
            if (isChild != null) {
                return isChild;
            }

            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.CHINESE);
            try {
                Date parse = simpleDateFormat.parse(birthday);
                isChild = DateTime.now().minusYears(12).isBefore(parse.getTime());
            } catch (ParseException e) {
                isChild = false;
            }
            return isChild;
        }
    }

    public List<PassengerBean> getPassengerList() {
        JSONArray passengerJsonArray = config.optJSONArray("passengers");
        List<PassengerBean> ret = new ArrayList<>();
        if (passengerJsonArray == null) {
            return ret;
        }

        for (int i = 0; i < passengerJsonArray.length(); i++) {
            JSONObject jsonObject = passengerJsonArray.optJSONObject(i);
            PassengerBean passengerBean = new PassengerBean();
            passengerBean.userName = jsonObject.optString("userName");
            if (passengerBean.userName.contains("/")) {
                passengerBean.userName = passengerBean.userName.toUpperCase();
            }
            passengerBean.gender = jsonObject.optString("gender");
            passengerBean.birthday = jsonObject.optString("birthday");
            passengerBean.certNumber = jsonObject.optString("certNumber");
            passengerBean.certType = jsonObject.optString("certType");
            passengerBean.certExpireDate = jsonObject.optString("certExpireDate");
            passengerBean.cardIssuePlace = jsonObject.optString("cardIssuePlace");

            ret.add(passengerBean);
        }
        return ret;
    }

    public void addPassenger(PassengerBean passengerBean) {
        JSONArray passengerJsonArray = config.optJSONArray("passengers");
//        List<PassengerBean> ret = new ArrayList<>();
        if (passengerJsonArray == null) {
            passengerJsonArray = new JSONArray();
            try {
                config.put("passengers", passengerJsonArray);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        boolean exist = false;
        for (int i = 0; i < passengerJsonArray.length(); i++) {
            JSONObject jsonObject = passengerJsonArray.optJSONObject(i);
            if (passengerBean.certNumber.equals(jsonObject.optString("certNumber"))) {
                write(passengerBean, jsonObject);
                exist = true;
                break;
            }
        }
        if (!exist) {
            JSONObject jsonObject = new JSONObject();
            write(passengerBean, jsonObject);
            passengerJsonArray.put(jsonObject);
        }
        save();
    }

    public void removePassenger(String certNumber) {
        JSONArray passengerJsonArray = config.optJSONArray("passengers");

        if (passengerJsonArray == null) {
            return;
        }
        for (int i = 0; i < passengerJsonArray.length(); i++) {
            JSONObject jsonObject = passengerJsonArray.optJSONObject(i);
            if (certNumber.equals(jsonObject.optString("certNumber"))) {
                passengerJsonArray.remove(i);
                save();
                return;
            }
        }
    }

    private void write(PassengerBean passengerBean, JSONObject jsonObject) {
        try {
            jsonObject.put("userName", passengerBean.userName);
            jsonObject.put("gender", passengerBean.gender);
            jsonObject.put("birthday", passengerBean.birthday);
            jsonObject.put("certNumber", passengerBean.certNumber);
            jsonObject.put("certType", passengerBean.certType);
            jsonObject.put("certExpireDate", passengerBean.certExpireDate);
            jsonObject.put("cardIssuePlace", passengerBean.cardIssuePlace);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public static class Contact {
        public String name = "";
        public String email = "";
        public String phone = "";
    }

    public Contact getContact() {
        JSONObject contactJson = config.optJSONObject("contact");
        Contact contact = new Contact();
        if (contactJson == null) {
            return contact;
        }
        contact.name = contactJson.optString("name");
        contact.email = contactJson.optString("email");
        contact.phone = contactJson.optString("phone");
        return contact;
    }

    public void updateContact(Contact contact) {
        JSONObject contactJson = config.optJSONObject("contact");

        if (contactJson == null) {
            contactJson = new JSONObject();
            try {
                config.put("contact", contactJson);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        try {
            contactJson.put("name", contact.name);
            contactJson.put("email", contact.email);
            contactJson.put("phone", contact.phone);
            save();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }


    public static class Setting {
        public String clientId = "";
        public int qps = 1000;
        public String multiDevice = "1";
    }

    public Setting getSetting() {
        JSONObject settingJson = config.optJSONObject("setting");
        Setting setting = new Setting();
        if (settingJson == null) {
            return setting;
        }
        setting.clientId = settingJson.optString("clientId");
        setting.qps = settingJson.optInt("qps", 1000);
        setting.multiDevice = settingJson.optString("multiDevice", "1");
        return setting;
    }

    public void updateSetting(Setting setting) {
        JSONObject settingJson = config.optJSONObject("setting");
        if (settingJson == null) {
            settingJson = new JSONObject();
            try {
                config.put("setting", settingJson);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        try {
            settingJson.put("clientId", setting.clientId);
            settingJson.put("qps", setting.qps);
            settingJson.put("multiDevice", setting.multiDevice);
            save();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
