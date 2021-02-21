package com.nilesh.btpoffline;

public class GeoMagReading {
    double mx;
    double my;
    double mz;
    double MA;

    GeoMagReading(double mx, double my, double mz) {
        this.mx = mx;
        this.my = my;
        this.mz = mz;
        this.MA = Math.sqrt(mx*mx + my*my + mz*mz);
    }

    public double getMA() {
        return MA;
    }

    public double getMx() {
        return mx;
    }

    public double getMy() {
        return my;
    }

    public double getMz() {
        return mz;
    }
}
