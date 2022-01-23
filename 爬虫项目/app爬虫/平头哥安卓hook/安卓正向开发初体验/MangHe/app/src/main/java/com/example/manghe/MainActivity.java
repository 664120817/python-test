package com.example.manghe;

import androidx.appcompat.app.AppCompatActivity;

import android.nfc.Tag;
import android.os.Bundle;
import android.util.Log;

public class MainActivity extends AppCompatActivity {

    static {
        System.loadLibrary("native-lib");
    }


    private static final String TAG= "manghe";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        MysteryBox box1 = new MysteryBox();
        Log.d(TAG,"onCreate:"+box1.toString());

        //静态方法
        String result1=MysteryBox.staticMethod("张三",200);
        Log.d(TAG,"onCreate:"+result1);
        String result2= box1.instanceMethod("李四",600);
        Log.d(TAG,"onCreate:"+result2);
        box1.callInnerClassMethod();
        Log.d(TAG,"onCreate:"+ nativeMathod());

//        MysteryBox box2 = new MysteryBox(1000);
//        Log.d(TAG,"onCreate:price="+box2.price);
//
//        MysteryBox box3 = new MysteryBox(1000, "测试");
//        Log.d(TAG, "onCreate:price="+box3.price+ ","+ box3.getBrand());

    }

    private native String nativeMathod();
}