package com.virjar.ratel.snkrs;

import android.util.Log;

import com.virjar.ratel.api.RatelToolKit;
import com.virjar.ratel.api.extension.superappium.PageTriggerManager;
import com.virjar.ratel.api.extension.superappium.SuperAppium;
import com.virjar.ratel.api.scheduler.RatelTask;
import com.virjar.ratel.snkrs.pages.TheWallActivityPageHandler;
import com.virjar.ratel.snkrs.pages.UniteActivityPageHandler;

import java.util.HashMap;
import java.util.Map;

import external.com.alibaba.fastjson.JSON;

public class SnkrsTaskScheduler implements RatelTask {
    @Override
    public Map<String, String> loadTaskParams() {
        Log.i(HookEntry.TAG, "scheduler task load task params");

        Map<String, String> ret = new HashMap<>();

        ret.put("snkrs_user_name", "13011860000");
        ret.put("snkrs_passworld", "yourPassword");
        ret.put("crawlId", "testCrawlId");
        // ratel. 开头的,是ratel定义的特殊标记
        ret.put("ratel.userId", "187821600000");
        return ret;
    }

    @Override
    public void doRatelTask(Map<String, String> params) {

        Log.i(HookEntry.TAG, "scheduler task with params:" + JSON.toJSONString(params));
        if (!params.containsKey("snkrs_user_name")) {
            //没有从服务器请求到任务，直接停止调度
            RatelToolKit.schedulerTaskBeanHandler.finishedMTask();
            return;
        }
        SuperAppium.TAG = HookEntry.TAG;
        GrabTaskBean.userName = params.get("snkrs_user_name");
        GrabTaskBean.password = params.get("snkrs_passworld");


        //ui点击控制
        setupUIDriver();
    }

    private void setupUIDriver() {
        PageTriggerManager.setTaskDuration(800);

        //启动页面,主要功能是发现有登陆按钮的话，跳转到登陆页面
        PageTriggerManager.addHandler("com.nike.snkrs.feed.activities.TheWallActivity",
                new TheWallActivityPageHandler()
        );

        //登陆页面，使用任务参数登陆账号，之后会回到主页面
        PageTriggerManager.addHandler("com.nike.unite.sdk.UniteActivity",
                new UniteActivityPageHandler()
        );

    }
}