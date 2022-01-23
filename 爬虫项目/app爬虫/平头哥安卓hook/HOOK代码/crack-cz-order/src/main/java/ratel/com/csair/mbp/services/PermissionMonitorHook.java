package ratel.com.csair.mbp.services;

import android.app.Activity;
import android.app.Fragment;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.support.annotation.RequiresApi;
import android.util.Log;

import com.virjar.ratel.api.rposed.RC_MethodHook;
import com.virjar.ratel.api.rposed.RposedBridge;

import java.util.Arrays;

import ratel.com.csair.mbp.HookEntry;

public class PermissionMonitorHook {

    public static void denyAllPermission() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) {
            return;
        }

        RposedBridge.hookAllMethods(Activity.class, "requestPermissions", new RC_MethodHook() {
            @Override
            protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) {
                    return;
                }
                param.setResult(null);
                final Activity activity = (Activity) param.thisObject;
                final String[] permissions = (String[]) param.args[0];
                Log.i(HookEntry.TAG, "Activity hook permissions " + Arrays.toString(permissions));
                final int requestCode = (int) param.args[1];
                final int[] ints = new int[permissions.length];
                Arrays.fill(ints, PackageManager.PERMISSION_DENIED);
                new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
                    @RequiresApi(api = Build.VERSION_CODES.M)
                    @Override
                    public void run() {
                        activity.onRequestPermissionsResult(requestCode, permissions, ints);
                    }
                }, 1500);
            }
        });

        RposedBridge.hookAllMethods(Fragment.class, "requestPermissions", new RC_MethodHook() {

            @Override
            protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) {
                    return;
                }
                param.setResult(null);
                final Fragment fragment = (Fragment) param.thisObject;
                final String[] permissions = (String[]) param.args[0];

                Log.i(HookEntry.TAG, "Fragment hook permissions " + Arrays.toString(permissions));
                final int requestCode = (int) param.args[1];
                final int[] ints = new int[permissions.length];
                Arrays.fill(ints, PackageManager.PERMISSION_DENIED);
                new Handler(Looper.getMainLooper()).postDelayed(new Runnable() {
                    @RequiresApi(api = Build.VERSION_CODES.M)
                    @Override
                    public void run() {
                        fragment.onRequestPermissionsResult(requestCode, permissions, ints);
                    }
                }, 1500);
            }

        });
    }
}
