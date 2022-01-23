#include <jni.h>
#include <jni.h>

//
// Created by Administrator on 2022/1/20 0020.
//
extern "C"
JNIEXPORT jstring JNICALL
Java_com_example_manghe_MainActivity_nativeMathod(JNIEnv *env, jobject thiz) {
    // TODO: implement nativeMathod()
    return env->NewStringUTF("我是一个native函数");

}



