# BLE Client for Wireless Soil Sensor

This BLE client is a part of a bigger project including wireless sensors.
It is sanning continuously for sensors ready to provide data, reading it and printitng into console.

- Read soil moisture sensor stats as a single structure: wakeup count, temperature, air pressure, humidity, soil moisture, battery level.
- Store sensor data into Kafka topic in Avro format.
- An option to read and change sensors wakeup interval in seconds.

## TODO

- Read sensors list from a file (JSON).
- Add topic name per sensor into configuration file.
- Read Kafka server paramters from a file (JSON)
- Read Avro schema from file.
