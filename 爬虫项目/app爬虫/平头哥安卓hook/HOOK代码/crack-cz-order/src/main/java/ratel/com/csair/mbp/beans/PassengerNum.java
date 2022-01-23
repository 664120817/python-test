package ratel.com.csair.mbp.beans;

public class PassengerNum {
    private int adultNum;
    private int childNum;
    private int infantNum;

    public int getAdultNum() {
        return adultNum;
    }

    public void setAdultNum(int adultNum) {
        this.adultNum = adultNum;
    }

    public int getChildNum() {
        return childNum;
    }

    public void setChildNum(int childNum) {
        this.childNum = childNum;
    }

    public int getInfantNum() {
        return infantNum;
    }

    public void setInfantNum(int infantNum) {
        this.infantNum = infantNum;
    }

    public PassengerNum(int adultNum, int childNum, int infantNum) {
        this.adultNum = adultNum;
        this.childNum = childNum;
        this.infantNum = infantNum;
    }
}