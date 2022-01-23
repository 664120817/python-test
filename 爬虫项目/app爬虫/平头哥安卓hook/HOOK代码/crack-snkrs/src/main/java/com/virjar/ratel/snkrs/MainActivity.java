package com.virjar.ratel.snkrs;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import com.virjar.ratel.crack.snkrs.BuildConfig;
import com.virjar.ratel.crack.snkrs.R;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView textView = findViewById(R.id.hint_text);
        textView.setText("SNKRS pluign:" + BuildConfig.VERSION_NAME);
    }
}
