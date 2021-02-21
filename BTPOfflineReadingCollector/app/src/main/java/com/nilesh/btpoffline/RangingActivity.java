package com.nilesh.btpoffline;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collection;

import android.app.Activity;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.RemoteException;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.altbeacon.beacon.Beacon;
import org.altbeacon.beacon.BeaconConsumer;
import org.altbeacon.beacon.BeaconManager;
import org.altbeacon.beacon.RangeNotifier;
import org.altbeacon.beacon.Region;
import org.w3c.dom.Text;

/**
 *
 * @author nilesh
 */

public class RangingActivity extends AppCompatActivity implements BeaconConsumer, SensorEventListener {
    protected static final String TAG = "RangingActivity";
    private BeaconManager beaconManager = BeaconManager.getInstanceForApplication(this);
    private SensorManager sensorManager = null;
    private Sensor mSensor = null;
    String magReading = "";
    private int beaconReadCount = 0;
    private int magReadCount = 0;
    public static final int maxReadCount = 50;
    private boolean fileWriteSuccess = true;
    TextView magneticTextView;
    TextView beaconTextView;
    Button saveButton;

    Coord coord;
    GeoMagReading geoMagReading;
    ArrayList<BeaconReading> beaconReadings;
    BeaconReading beaconReading;
    BeaconReadingOneScan beaconReadingOneScan;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ranging);

        magneticTextView = (TextView) findViewById(R.id.magneticTextView);
        beaconTextView = (TextView) findViewById(R.id.beaconTextView);

        magneticTextView.setMovementMethod(new ScrollingMovementMethod());
        beaconTextView.setMovementMethod(new ScrollingMovementMethod());

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        mSensor = MonitoringActivity.currSensor;

        saveButton = (Button) findViewById(R.id.saveButton);
        saveButton.setEnabled(false);

        coord = new Coord(MonitoringActivity.x_coord, MonitoringActivity.y_coord);

        saveButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                File folder = getExternalFilesDir("BTP");// Folder Name
                File myFile = new File(folder, "myReading_" + MonitoringActivity.x_coord + "_" + MonitoringActivity.y_coord + ".json");
                try {
                    new FileOutputStream(myFile).close();
                    writeReadingData(myFile);
                } catch (IOException e) {
                    Toast.makeText(v.getContext(), "Error saving data to file. Data in file may not be correct.", Toast.LENGTH_SHORT).show();
                }
                finish();
                // use finish() instead of startActivity() to maintain the state of
                // previous activity from which this activity was called.
            }
        });
    }

    @Override 
    protected void onDestroy() {
        super.onDestroy();
    }

    @Override 
    protected void onPause() {
        super.onPause();
        beaconManager.unbind(this);
        sensorManager.unregisterListener(this);
    }

    @Override 
    protected void onResume() {
        super.onResume();
        beaconManager.bind(this);
        if(MonitoringActivity.currSensor != null) {
            sensorManager.registerListener(this, mSensor, SensorManager.SENSOR_DELAY_UI);
        }
    }

    @Override
    public void onStart() {
        super.onStart();
        beaconManager.bind(this);
        if(MonitoringActivity.currSensor != null) {
            sensorManager.registerListener(this, mSensor, SensorManager.SENSOR_DELAY_UI);
        }
    }

    @Override
    public void onStop() {
        super.onStop();
        beaconManager.unbind(this);
        sensorManager.unregisterListener(this);
    }

    @Override
    public void onBeaconServiceConnect() {

        RangeNotifier rangeNotifier = new RangeNotifier() {
           @Override
           public void didRangeBeaconsInRegion(Collection<Beacon> beacons, Region region) {
               if(beaconReadCount >= maxReadCount) {
                   enableButton();
                   return;
               }
               if (beacons.size() > 0) {
                  // Log.d(TAG, "didRangeBeaconsInRegion called with beacon count:  "+beacons.size());
                  logToDisplay("reading - " + String.valueOf(beaconReadCount+1));
                  logToDisplay("numOfBeacons = " + beacons.size());

                  int beaconNo = 0;
                  beaconReadings = new ArrayList<>();
                  for(Beacon xx : beacons)
                  {
                      beaconNo++;
                      logToDisplay("The  beacon   "+ beaconNo +" no. AND MY Minor is " + xx.getId3() + "  .");
                      logToDisplay("My MAC ADDRESS is " + xx.getBluetoothAddress() + "  .");
                      logToDisplay("My RSSI is " + xx.getRssi() + "  .");

                      beaconReading = new BeaconReading(xx.getId1(), xx.getId2(), xx.getId3(), xx.getRssi(), xx.getBluetoothAddress(), xx.getDistance());
                      beaconReadings.add(beaconReading);
                  }
                  logToDisplay("");

                  beaconReadingOneScan = new BeaconReadingOneScan(beaconReadings);
                  coord.setBeaconReadingOneScanAtIdx(beaconReadingOneScan, beaconReadCount);
                  beaconReadCount++;
               }
           }

        };

        try {
            beaconManager.startRangingBeaconsInRegion(new Region("myRangingUniqueId", null, null, null));
            beaconManager.addRangeNotifier(rangeNotifier);
        } catch (RemoteException e) {   }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if(magReadCount >= maxReadCount) {
            enableButton();
            sensorManager.unregisterListener(this);
            return;
        }

//        int sensorType = event.sensor.getType(); // type of sensor - use this to understand and format readings
//        float timeOfReading = event.timestamp; // timestamp of the event when reading was captured
//        int accuracyOfReading = event.accuracy; // accuracy of reading (0 = unreliable, 1 = low, 2 = medium, 3 = high)
        int x = event.values.length; // the length of the reading values array

        magReading = "";
        for(int i=0; i<x; i++) {
            magReading += String.valueOf(i+1) + ".  " + String.valueOf(event.values[i]) + "\n";
        }

        magneticTextView.append("reading - " + String.valueOf(magReadCount+1) + "\n");
        magneticTextView.append(magReading);
        magneticTextView.append("\n");

        geoMagReading = new GeoMagReading(event.values[0], event.values[1], event.values[2]);
        coord.setGeoMagReadingAtIdx(geoMagReading, magReadCount);

        magReadCount++;
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Nothing to be done here
    }

    private void logToDisplay(final String line) {
        runOnUiThread(new Runnable() {
            public void run() {
                beaconTextView.append(line+"\n");
            }
        });
    }

    private void writeData(File myFile, String data) {
        if(fileWriteSuccess == true) {
            FileOutputStream fileOutputStream = null;
            try {
                fileOutputStream = new FileOutputStream(myFile, true);
                fileOutputStream.write(data.getBytes());
            } catch (Exception e) {
                fileWriteSuccess = false;
            } finally {
                if (fileOutputStream != null) {
                    try {
                        fileOutputStream.close();
                    } catch (IOException e) {
                        fileWriteSuccess = false;
                    }
                }
            }
        }
    }

    private void writeReadingData(File myFile) {
        fileWriteSuccess = true;
        writeData(myFile, "{");

        writeData(myFile, "\t\"x-coord\": " + String.valueOf(coord.getCoord_x()) + ",\n");
        writeData(myFile, "\t\"y-coord\": " + String.valueOf(coord.getCoord_y()) + ",\n");

        int readCount = 0;
        writeData(myFile, "\t\"geoMagReadings\": [\n");
        for(GeoMagReading xx : coord.getGeoMagReadings()) {
            readCount++;
            writeData(myFile, "\t\t{\n");
            writeData(myFile, "\t\t\t\"mx\": " + String.valueOf(xx.getMx()) + ",\n");
            writeData(myFile, "\t\t\t\"my\": " + String.valueOf(xx.getMy()) + ",\n");
            writeData(myFile, "\t\t\t\"mz\": " + String.valueOf(xx.getMz()) + ",\n");
            writeData(myFile, "\t\t\t\"MA\": " + String.valueOf(xx.getMA()) + "\n");
            if(readCount == maxReadCount) {
                writeData(myFile, "\t\t}\n");
            }
            else {
                writeData(myFile, "\t\t},\n");
            }
        }
        writeData(myFile, "\t],\n");

        readCount = 0;
        int beaconCount;
        int totalBeacons;
        writeData(myFile, "\t\"beaconReadings\": [\n");
        for(BeaconReadingOneScan xx : coord.getBeaconReadingOneScans()) {
            readCount++;
            totalBeacons = xx.getBeaconReadings().size();
            writeData(myFile, "\t\t{\n");
            writeData(myFile, "\t\t\t\"numOfBeacons\": " + String.valueOf(totalBeacons) + ",\n");
            writeData(myFile, "\t\t\t\"readings\": [\n");
            beaconCount = 0;
            for(BeaconReading yy : xx.getBeaconReadings()) {
                beaconCount++;
                writeData(myFile, "\t\t\t\t{\n");
                writeData(myFile, "\t\t\t\t\t\"id1\": \"" + String.valueOf(yy.getId1()) + "\",\n");
                writeData(myFile, "\t\t\t\t\t\"id2\": " + String.valueOf(yy.getId2()) + ",\n");
                writeData(myFile, "\t\t\t\t\t\"id3\": " + String.valueOf(yy.getId3()) + ",\n");
                writeData(myFile, "\t\t\t\t\t\"address\": \"" + String.valueOf(yy.getAddress()) + "\",\n");
                writeData(myFile, "\t\t\t\t\t\"rssi\": " + String.valueOf(yy.getRssi()) + ",\n");
                writeData(myFile, "\t\t\t\t\t\"distance\": " + String.valueOf(yy.getDistance()) + "\n");
                if(beaconCount == totalBeacons) {
                    writeData(myFile, "\t\t\t\t}\n");
                }
                else {
                    writeData(myFile, "\t\t\t\t},\n");
                }
            }
            writeData(myFile, "\t\t\t]\n");
            if(readCount == maxReadCount) {
                writeData(myFile, "\t\t}\n");
            }
            else {
                writeData(myFile, "\t\t},\n");
            }
        }
        writeData(myFile, "\t]\n");

        writeData(myFile, "}");

        if(fileWriteSuccess == true) {
            Toast.makeText(this, "Done" + myFile.getAbsolutePath(), Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(this, "Error saving data to file. Data in file may not be correct.", Toast.LENGTH_SHORT).show();
        }
    }

    private void enableButton() {
        if(beaconReadCount >= maxReadCount && magReadCount >= maxReadCount) {
            saveButton.setEnabled(true);
        }
    }
}
