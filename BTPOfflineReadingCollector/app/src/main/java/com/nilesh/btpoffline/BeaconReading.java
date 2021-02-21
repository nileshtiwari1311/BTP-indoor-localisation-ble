package com.nilesh.btpoffline;

public class BeaconReading {
    org.altbeacon.beacon.Identifier id1;
    org.altbeacon.beacon.Identifier id2;
    org.altbeacon.beacon.Identifier id3; // beacon number
    int rssi;
    String address;
    double distance;

    BeaconReading(org.altbeacon.beacon.Identifier id1, org.altbeacon.beacon.Identifier id2, org.altbeacon.beacon.Identifier id3, int rssi, String address, double distance) {
        this.id1 = id1;
        this.id2 = id2;
        this.id3 = id3;
        this.rssi = rssi;
        this.address = address;
        this.distance = distance;
    }

    public String getAddress() {
        return address;
    }

    public org.altbeacon.beacon.Identifier getId1() {
        return id1;
    }

    public double getDistance() {
        return distance;
    }

    public org.altbeacon.beacon.Identifier getId2() {
        return id2;
    }

    public org.altbeacon.beacon.Identifier getId3() {
        return id3;
    }

    public int getRssi() {
        return rssi;
    }
}
