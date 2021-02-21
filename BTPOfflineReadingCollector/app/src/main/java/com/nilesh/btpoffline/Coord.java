package com.nilesh.btpoffline;

public class Coord {
    int coord_x;
    int coord_y;
    GeoMagReading[] geoMagReadings;
    BeaconReadingOneScan[] beaconReadingOneScans;

    Coord(int x, int y){
        coord_x = x;
        coord_y = y;
        geoMagReadings = new GeoMagReading[RangingActivity.maxReadCount];
        beaconReadingOneScans = new BeaconReadingOneScan[RangingActivity.maxReadCount];
    }

    public int getCoord_x() {
        return coord_x;
    }

    public int getCoord_y() {
        return coord_y;
    }

    public BeaconReadingOneScan[] getBeaconReadingOneScans() {
        return beaconReadingOneScans;
    }

    public GeoMagReading[] getGeoMagReadings() {
        return geoMagReadings;
    }

    public void setGeoMagReadingAtIdx(GeoMagReading geoMagReading, int id) {
        this.geoMagReadings[id] = geoMagReading;
    }

    public void setBeaconReadingOneScanAtIdx(BeaconReadingOneScan beaconReadingOneScan, int id) {
        this.beaconReadingOneScans[id] = beaconReadingOneScan;
    }
}
