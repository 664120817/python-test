package ratel.com.csair.mbp.beans;


import java.util.HashMap;
import java.util.Map;

public class PassengerAdaptor {


    //乘机人类型
    //成人
    public static final String PSG_ADT = "ADT";
    //儿童
    public static final String PSG_CHD = "CHD";
    //婴儿
    public static final String PSG_INF = "INF";

    //身份证
    private static final String CARDTYPE_ID = "NI";
    //护照
    private static final String CARDTYPE_PASSPORT = "PP";
    //其他
    private static final String CARDTYPE_OTHER = "OTHER";


    private static final String MAN = "M";
    private static final String WOMAN = "F";

    private static final Map<Integer, String> PASSENGER_TYPE_MAPPER = new HashMap<>();

    private static final Map<Integer, String> ID_TYPE_MAPPER = new HashMap<>();
    private static final Map<String, String> ID_TYPE_MAPPER_STR = new HashMap<>();

    private static final Map<Integer, String> SEX_MAPPER = new HashMap<>();
    private static final Map<String, String> SEX_MAPPER_STR = new HashMap<>();

    public static String getPassengerType(int passengerType) {
        return PASSENGER_TYPE_MAPPER.get(passengerType);
    }

    public static String getIdType(int idType) {
        return ID_TYPE_MAPPER.get(idType);
    }

    public static String getIdType(String idType) {
        return ID_TYPE_MAPPER_STR.get(idType);
    }

    public static String getSexType(int type) {
        return SEX_MAPPER.get(type);
    }

    public static String getSexType(String type) {
        return SEX_MAPPER_STR.get(type);
    }

    public static final int PASSENGER_TYPE_ADULT = 0;
    public static final int PASSENGER_TYPE_CHILD = 1;
    public static final int PASSENGER_TYPE_INFANT = 2;

    public static final int CARD_TYPE_ID = 0;
    public static final int CARD_TYPE_PASSPORT = 1;
    public static final int CARD_TYPE_OTHER = 2;

    public static final int GENDER_MALE = 0;
    public static final int GENDER_FEMALE = 1;

    static {
        PASSENGER_TYPE_MAPPER.put(PASSENGER_TYPE_ADULT, PSG_ADT);
        PASSENGER_TYPE_MAPPER.put(PASSENGER_TYPE_CHILD, PSG_CHD);
        PASSENGER_TYPE_MAPPER.put(PASSENGER_TYPE_INFANT, PSG_INF);

        ID_TYPE_MAPPER.put(CARD_TYPE_ID, CARDTYPE_ID);
        ID_TYPE_MAPPER.put(CARD_TYPE_PASSPORT, CARDTYPE_PASSPORT);
        ID_TYPE_MAPPER.put(CARD_TYPE_OTHER, CARDTYPE_OTHER);

        ID_TYPE_MAPPER_STR.put("身份证", CARDTYPE_ID);
        ID_TYPE_MAPPER_STR.put("护照", CARDTYPE_PASSPORT);
        ID_TYPE_MAPPER_STR.put("其他", CARDTYPE_OTHER);

        SEX_MAPPER.put(GENDER_MALE, MAN);
        SEX_MAPPER.put(GENDER_FEMALE, WOMAN);

        SEX_MAPPER_STR.put("男", MAN);
        SEX_MAPPER_STR.put("女", WOMAN);
    }
}