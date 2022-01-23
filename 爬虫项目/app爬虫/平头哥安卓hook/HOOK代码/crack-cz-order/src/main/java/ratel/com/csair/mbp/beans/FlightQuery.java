package ratel.com.csair.mbp.beans;

public class FlightQuery {
    private String arrCityNameZH;
    private String depCityNameZH;
    private String depAirportCode;
    private String arrAirportCode;

    public void setArrCityNameZH(String arrCityNameZH) {
        this.arrCityNameZH = arrCityNameZH;
    }

    public void setDepCityNameZH(String depCityNameZH) {
        this.depCityNameZH = depCityNameZH;
    }

    public void setDepAirportCode(String depAirportCode) {
        this.depAirportCode = depAirportCode;
    }

    public void setArrAirportCode(String arrAirportCode) {
        this.arrAirportCode = arrAirportCode;
    }

    public String getArrCityNameZH() {
        return arrCityNameZH;
    }

    public String getDepCityNameZH() {
        return depCityNameZH;
    }

    public String getDepAirportCode() {
        return depAirportCode;
    }

    public String getArrAirportCode() {
        return arrAirportCode;
    }


}
