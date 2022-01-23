package com.example.manghe;

import android.nfc.Tag;
import android.util.Log;

import java.util.Random;

public class MysteryBox {
    private final static String TAG ="manghe";
    private final String content;
    private boolean isOpened;
    public final int price;
    private final String brand;
    private final static int BASE_PRICE=10;


    public MysteryBox(){
        this.price =BASE_PRICE;
        this.brand ="手办盲盒";



        isOpened=false;
        int random = new Random().nextInt();
        if(random%100 ==1){
            content = "隐藏属性";

        }else {
            content = "普通属性";

        }
    }
    private MysteryBox(String brand){
        this.price=10;
        this.brand =brand;

        isOpened=false;
        int random = new Random().nextInt();
        if(random%100 ==1){
            content = "隐藏属性";

        }else {
            content = "普通属性";

        }


    }

    public MysteryBox(int price){
        this.price=price;
        this.brand ="手办盲盒";

        isOpened=false;
        int random = new Random().nextInt();
        int p =100;
        if (price>100){
            p=10;

        }
        if(random%p ==1){
            content = "隐藏属性";

        }else {
            content = "普通属性";

        }
    }

    public MysteryBox(int price,String brand){
        this.price=price;
        this.brand =brand;

        isOpened=false;
        int random = new Random().nextInt();
        int p =100;
        if (price>100){
            p=10;

        }
        if(random%p ==1){
            content = "隐藏属性";

        }else {
            content = "普通属性";

        }


    }

    public void open(){
        isOpened =true;
    }

    private void close(){
        isOpened=false;
    }
    public String getContent(){

        if(isOpened){

            return content;
        }
        return "这个盲盒没有打开哦";
    }
public String getBrand(){
        return brand;

}
 //静态方法的HOOK
    public static  String staticMethod(String name,int price){
        Log.d(TAG,"staticMethod:name= " +name+",price="+price);
        return "我是静态方法的返回值";

    }
    //实例方法的hook
    public String instanceMethod(String name , int price){
        Log.d(TAG,"instanceMethod:name="+name+",price="+price);
        return "我是实例方法的返回值";
    }
    //内部类处理
    static class InnerClass{
        private String innerClassMethod(String name ,int price){
            Log.d(TAG,"innerClassMethod:name= " +name+",price="+price);
            return "我是内部类的返回值";
        }
    }
    public void callInnerClassMethod(){
        InnerClass innerClass =new InnerClass();
        Log.d(TAG,"callInnerClassMethod"+innerClass.innerClassMethod("王五",1000));
    }



    @Override
    public String toString() {
        return "MysteryBox{" +
                "content='" + content + '\'' +
                ", isOpened=" + isOpened +
                ", price=" + price +
                ", brand='" + brand + '\'' +
                '}';
    }


}
