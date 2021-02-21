package com.nilesh.btpoffline;

import java.util.ArrayList;

public class BeaconReadingOneScan {
    ArrayList<BeaconReading> beaconReadings;

    BeaconReadingOneScan(ArrayList<BeaconReading> r) {
        beaconReadings = r;
    }

    public ArrayList<BeaconReading> getBeaconReadings() {
        return beaconReadings;
    }
}
