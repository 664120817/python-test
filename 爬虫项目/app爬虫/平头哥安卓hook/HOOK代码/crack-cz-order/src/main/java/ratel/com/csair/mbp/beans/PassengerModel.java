package ratel.com.csair.mbp.beans;

import external.com.alibaba.fastjson.annotation.JSONField;

public class PassengerModel {
    private String babyCarry = "";
    private String bcId = "";
    private String birthdayDate;
    private String carrierPsgId = "";
    private String carrierPsgName;
    private String certIssueCountry;
    private String certNum;
    private String certPeriodValidityDate;
    private String certType;
    private String channelId = "";
    private String createId = "";
    private String dCity = "";
    private String dCountry = "";
    private String dDetailAddress = "";
    private String dPostCode = "";
    private String dProvince = "";
    private String email = "";
    private String fpCardNo = "";
    private String fpCompany;
    private String gender;
    @JSONField(name = "isAdult")
    private boolean isAdult;
    @JSONField(name= "isChecked")
    private boolean isChecked;
    @JSONField(name = "isInternational")
    private String isInternational;
    @JSONField( name = "isUserFreightCoupon")
    private boolean isUserFreightCoupon;
    private String mobilePhone = "";
    private String nationality;
    private String opId = "";
    private String psgId = "";
    private String psgName;
    private String psgType;
    private String rCity = "";
    private String rCountry = "";
    private String rPostCode = "";
    private String rProvince = "";
    private String rdetailAddress = "";
    private String userId;
    private String userIdType = "";

    public PassengerModel(String birthdayDate, String certIssueCountry, String certNum, String certPeriodValidityDate, String certType, String gender, boolean isAdult, String nationality, String psgName, String userId) {
        this.birthdayDate = birthdayDate;
        this.certIssueCountry = certIssueCountry;
        this.certNum = certNum;
        this.certPeriodValidityDate = certPeriodValidityDate;
        this.certType = certType;
        this.gender = gender;
        this.isAdult = isAdult;
        this.nationality = nationality;
        this.psgName = psgName.toUpperCase();
        this.userId = userId;

        this.carrierPsgName = "请选择";
        this.fpCompany = "CZ";
        this.isChecked = false;
        this.isInternational = "1";
        this.isUserFreightCoupon = false;
        this.psgType = "0";
    }

    public String getBabyCarry() {
        return babyCarry;
    }

    public void setBabyCarry(String babyCarry) {
        this.babyCarry = babyCarry;
    }

    public String getBcId() {
        return bcId;
    }

    public void setBcId(String bcId) {
        this.bcId = bcId;
    }

    public String getBirthdayDate() {
        return birthdayDate;
    }

    public void setBirthdayDate(String birthdayDate) {
        this.birthdayDate = birthdayDate;
    }

    public String getCarrierPsgId() {
        return carrierPsgId;
    }

    public void setCarrierPsgId(String carrierPsgId) {
        this.carrierPsgId = carrierPsgId;
    }

    public String getCarrierPsgName() {
        return carrierPsgName;
    }

    public void setCarrierPsgName(String carrierPsgName) {
        this.carrierPsgName = carrierPsgName;
    }

    public String getCertIssueCountry() {
        return certIssueCountry;
    }

    public void setCertIssueCountry(String certIssueCountry) {
        this.certIssueCountry = certIssueCountry;
    }

    public String getCertNum() {
        return certNum;
    }

    public void setCertNum(String certNum) {
        this.certNum = certNum;
    }

    public String getCertPeriodValidityDate() {
        return certPeriodValidityDate;
    }

    public void setCertPeriodValidityDate(String certPeriodValidityDate) {
        this.certPeriodValidityDate = certPeriodValidityDate;
    }

    public String getCertType() {
        return certType;
    }

    public void setCertType(String certType) {
        this.certType = certType;
    }

    public String getChannelId() {
        return channelId;
    }

    public void setChannelId(String channelId) {
        this.channelId = channelId;
    }

    public String getCreateId() {
        return createId;
    }

    public void setCreateId(String createId) {
        this.createId = createId;
    }

    public String getdCity() {
        return dCity;
    }

    public void setdCity(String dCity) {
        this.dCity = dCity;
    }

    public String getdCountry() {
        return dCountry;
    }

    public void setdCountry(String dCountry) {
        this.dCountry = dCountry;
    }

    public String getdDetailAddress() {
        return dDetailAddress;
    }

    public void setdDetailAddress(String dDetailAddress) {
        this.dDetailAddress = dDetailAddress;
    }

    public String getdPostCode() {
        return dPostCode;
    }

    public void setdPostCode(String dPostCode) {
        this.dPostCode = dPostCode;
    }

    public String getdProvince() {
        return dProvince;
    }

    public void setdProvince(String dProvince) {
        this.dProvince = dProvince;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFpCardNo() {
        return fpCardNo;
    }

    public void setFpCardNo(String fpCardNo) {
        this.fpCardNo = fpCardNo;
    }

    public String getFpCompany() {
        return fpCompany;
    }

    public void setFpCompany(String fpCompany) {
        this.fpCompany = fpCompany;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public boolean isAdult() {
        return isAdult;
    }

    public void setAdult(boolean adult) {
        isAdult = adult;
    }

    public boolean isChecked() {
        return isChecked;
    }

    public void setChecked(boolean checked) {
        isChecked = checked;
    }

    public String getIsInternational() {
        return isInternational;
    }

    public void setIsInternational(String isInternational) {
        this.isInternational = isInternational;
    }

    public boolean isUserFreightCoupon() {
        return isUserFreightCoupon;
    }

    public void setUserFreightCoupon(boolean userFreightCoupon) {
        isUserFreightCoupon = userFreightCoupon;
    }

    public String getMobilePhone() {
        return mobilePhone;
    }

    public void setMobilePhone(String mobilePhone) {
        this.mobilePhone = mobilePhone;
    }

    public String getNationality() {
        return nationality;
    }

    public void setNationality(String nationality) {
        this.nationality = nationality;
    }

    public String getOpId() {
        return opId;
    }

    public void setOpId(String opId) {
        this.opId = opId;
    }

    public String getPsgId() {
        return psgId;
    }

    public void setPsgId(String psgId) {
        this.psgId = psgId;
    }

    public String getPsgName() {
        return psgName;
    }

    public void setPsgName(String psgName) {
        this.psgName = psgName;
    }

    public String getPsgType() {
        return psgType;
    }

    public void setPsgType(String psgType) {
        this.psgType = psgType;
    }

    public String getrCity() {
        return rCity;
    }

    public void setrCity(String rCity) {
        this.rCity = rCity;
    }

    public String getrCountry() {
        return rCountry;
    }

    public void setrCountry(String rCountry) {
        this.rCountry = rCountry;
    }

    public String getrPostCode() {
        return rPostCode;
    }

    public void setrPostCode(String rPostCode) {
        this.rPostCode = rPostCode;
    }

    public String getrProvince() {
        return rProvince;
    }

    public void setrProvince(String rProvince) {
        this.rProvince = rProvince;
    }

    public String getRdetailAddress() {
        return rdetailAddress;
    }

    public void setRdetailAddress(String rdetailAddress) {
        this.rdetailAddress = rdetailAddress;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getUserIdType() {
        return userIdType;
    }

    public void setUserIdType(String userIdType) {
        this.userIdType = userIdType;
    }
}