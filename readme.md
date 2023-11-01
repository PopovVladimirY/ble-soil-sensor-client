# BLE Client for Wireless Soil Sensor

This BLE client is a part of a bigger project including wireless sensors.
It is sanning continuously for sensors ready to provide data, reading it and printitng into console.

- Read soil moisture sensor stats as a single structure: wakeup count, temperature, air pressure, humidity, soil moisture, battery level.
- Store sensor data into Kafka topic in Avro format.
- An option to read and change sensors wakeup interval in seconds.


## Handling OS Caching of BLE Device Services

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
