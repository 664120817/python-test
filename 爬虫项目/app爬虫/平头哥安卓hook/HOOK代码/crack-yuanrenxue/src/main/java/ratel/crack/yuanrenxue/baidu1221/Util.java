package ratel.crack.yuanrenxue.baidu1221;

import external.org.apache.commons.lang3.tuple.Pair;

public class Util {

    static int height = 2340;
    static int width = 1080;

    public static Pair<Pair<Double, Double>, Pair<Double, Double>> getQueryScope(double lng, double lat, int level) {
        Pair<Double, Double> bottomLeft = bottomLeft(lng, lat, level);
        Pair<Double, Double> topRight = topRight(lng, lat, 17);
        return Pair.of(bottomLeft, topRight);
    }


    public static Pair<Double, Double> bottomLeft(double lng, double lat, int level) {
        double l = getZoomUnits(level);
        double resultLng = lng - l * (width / 2);
        double resultLat = lat - l * (height / 2);
        return Pair.of(resultLng, resultLat);
    }

    public static Pair<Double, Double> topRight(double lng, double lat, int level) {
        double l = getZoomUnits(level);
        double resultLng = lng + l * (width / 2);
        double resultLat = lat + l * (height / 2);
        return Pair.of(resultLng, resultLat);
    }

    public static double getZoomUnits(int level) {
        return Math.pow(2, 18 - level);
    }

}
