package ratel.com.csair.mbp.services;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Color;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedHelpers;

import java.util.List;
import java.util.Set;

import io.netty.util.internal.ConcurrentSet;
import ratel.com.csair.mbp.beans.PassengerNum;


/**
 * Created by virjar on 2017/12/23.<br/>
 *
 * @author virjar
 */
class ActivityHooker {
    @SuppressLint("StaticFieldLeak")
    private static TextView sTextView = null;
    private static String sActivityName = null;
    private static String sViewName = null;
    static Set<String> sFragments = new ConcurrentSet<>();
    private static Set<Class> hookedClass = new ConcurrentSet<>();
    private static ResumeHookCallBack resumeHookCallBack = new ResumeHookCallBack();

    private static class ResumeHookCallBack extends RC_MethodHook {
        @Override
        protected void afterHookedMethod(MethodHookParam param) throws Throwable {
            super.afterHookedMethod(param);
            Object hasCalled = param.getObjectExtra("hasCalled");
            if (hasCalled != null) {
                return;
            }
            param.setObjectExtra("hasCalled", "true");
            Activity activity = (Activity) param.thisObject;
            addTextView(activity);
        }
    }

    static void hookActivity() {
        RposedHelpers.findAndHookMethod(Activity.class, "onResume", resumeHookCallBack);
    }

    private static void addTextView(Activity activity) {
        if (sTextView == null) {
            genTextView(activity);
        }
        if (sTextView.getParent() != null) {
            ViewParent parent = sTextView.getParent();
            if (parent instanceof ViewGroup) {
                ((ViewGroup) parent).removeView(sTextView);
            }
        }
        FrameLayout frameLayout = (FrameLayout) activity.getWindow().getDecorView();
        frameLayout.addView(sTextView);
        updatePanel("none");
        sTextView.bringToFront();
    }


    private static void genTextView(Activity activity) {
        sTextView = new TextView(activity);
        sTextView.setTextSize(16f);
        // int y =  activity.getWindow().getDecorView().getHeight() -200;
        sTextView.setY(48 * 12f);
        sTextView.setBackgroundColor(Color.parseColor("#cc888888"));
        sTextView.setTextColor(Color.WHITE);
        sTextView.setLayoutParams(new FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT,
                FrameLayout.LayoutParams.WRAP_CONTENT));


        sTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                StringBuilder fragments = new StringBuilder();
                for (String fragment : sFragments) {
                    fragments.append(fragment).append("\n");// += fragment + "\n";
                }

                if (fragments.length() > 0) {
                    Toast.makeText(sTextView.getContext(), fragments, Toast.LENGTH_LONG).show();
                }
            }
        });
    }


    public static void appendPanel(final String message) {
        if (sTextView == null) {
            return;
        }
        new Handler(Looper.getMainLooper()).post(new Runnable() {
            @SuppressLint("SetTextI18n")
            @Override
            public void run() {
                CharSequence text = sTextView.getText();
                sTextView.setText(text + "\n" + message);
            }
        });
    }

    public static void updatePanel(final String message) {
        if (sTextView == null) {
            return;
        }
        new Handler(Looper.getMainLooper()).post(new Runnable() {
            @Override
            public void run() {
                ConfigManager.TripBean tripConfig = ConfigManager.getInstance().getTripConfig();
                PassengerNum passengerNum = computePassengerNum(ConfigManager.getInstance().getPassengerList());
                String totalMessage = tripConfig.dep + "-" + tripConfig.arr + " " + tripConfig.flightNumber + "\n"
                        + tripConfig.depDate + "  adt:" + passengerNum.getAdultNum() + " child:" + passengerNum.getChildNum() + "\n"
                        + message;

                sTextView.setText(totalMessage);
            }
        });

        //sTextView.invalidate();
    }


    private static PassengerNum computePassengerNum(List<ConfigManager.PassengerBean> passengerList) {
        int adultNum = 0;
        int childNum = 0;
        int infantNum = 0;
        for (ConfigManager.PassengerBean passenger : passengerList) {
            if (passenger.getIsChild()) {
                childNum++;
            } else {
                adultNum++;
            }
        }
        return new PassengerNum(adultNum, childNum, infantNum);
    }

}
