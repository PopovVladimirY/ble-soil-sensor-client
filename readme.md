# BLE Client for Wireless Sensor

This BLE client is a part of a bigger project for handling wireless sensors. The sensors are in a deep sleep mode for most of the time, waking up for a short moment to do the measuremens and send them to avaitng BLI client. The BLE client in turn is sanning continuously for sensors ready to provide data, reading the stats from the discovered sensor, sending this data to Kafka messaging server, and printitng it into console for info.

The exact wireless sensor used in the project is a custom made soil moisture sensor which is capable of measuring ambient temperature, humidity, and air pressure in addition to the main function of monitoring soil moisuter level.

The BLE client on its side is made to:
- Read each sensor stats as a single structure containing: wakeup count, temperature, air pressure, humidity, soil moisture, and battery level.
- Store sensor data into Kafka topic in Avro format.
- As an option, read and change sensors deep sleep interval in seconds.

## Sensors vs BLE Client communication

Because sensors are in a deep sleep most of the time, the BLE communication has to be taken care of with this in mind. The sensors do not require authentication and there is no pairing as such. Instead, the sensors' **device type** is provided to the client in configuration and continuous scanning is ran. When a BLE device with the right name is found, a connection is established and the client is reading sensor's stats closing connection as it is done. The sensor in turn, when coming out of the deep sleep will wait for client connection for a short interval (~30 sec). It will go back to low power mode on timeout or, if client connected during sensor wait inteval, the client requiesting to disconnect. Powering sensor down on client dissconnection will extend the battery live time.

## Dependencies

In addition to standad Python packages, like *io*, *datetime*, this project depends on the following 3d-party packages:

1. Bleak - BLE library for Python.
```
    pip install bleak
```
2. Kafka - There are few Python intgegration flawors available for Kafka. *python-kafka* and *confluent-kafka*. The former is used in this project.
```
    pip install python-kafka
```
3. Avro - Avro schema is used to package topic data before sending it to Kafka.
```
    pip install avro
```
4. numpy - is used for parsing BLE raw data.
```
    pip install numpy
```

## Handling OS Caching of BLE Device Services

    https://bleak.readthedocs.io/en/latest/troubleshooting.html#common-mistakes

If you develop your own BLE peripherals, and frequently change services, characteristics and/or descriptors, then Bleak might report outdated versions of your peripheral’s services due to OS level caching. The caching is done to speed up the connections with peripherals where services do not change and is enabled by default on most operating systems and thus also in Bleak.

There are ways to avoid this on different backends though, and if you experience these kinds of problems, the steps below might help you to circumvent the caches.

**macOS**
The OS level caching handling on macOS has not been explored yet.

**Linux**
When you change the structure of services/characteristics on a device, you have to remove the device from BlueZ so that it will read everything again. Otherwise BlueZ gives the cached values from the first time the device was connected. You can use the bluetoothctl command line tool to do this:

bluetoothctl -- remove XX:XX:XX:XX:XX:XX

**prior to BlueZ 5.62 you also need to manually delete the GATT cache**
    sudo rm "/var/lib/bluetooth/YY:YY:YY:YY:YY:YY/cache/XX:XX:XX:XX:XX:XX"

…where XX:XX:XX:XX:XX:XX is the Bluetooth address of your device and YY:YY:YY:YY:YY:YY is the Bluetooth address of the Bluetooth adapter on your computer.


## TODO

- Read sensors list from a file (JSON).
- Add topic name per sensor into configuration file.
- Read Kafka server paramters from a file (JSON)
- Read Avro schema from file.
