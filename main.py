import asyncio
import numpy as np
import datetime 
from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic, BleakGATTServiceCollection
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import io
import avro.schema
from avro.io import DatumWriter


t_uuid: str = '9b5099ae-10f0-4a78-a8b7-eb086e3cb69b'
sleep_uuid: str = '54021135-c289-4e63-af8e-653f32e7851a'

broker='192.168.200.12:9092'
client_id = 'msensor1_id'
msensor1_topic = "msensor1_live_topic"

avro_schema = '''{
    "namespace": "msensor.avro",
    "type": "record",
    "name": "msensor",
    "fields": [
        {"name": "timestamp", "type": ["float", "null"]},
        {"name": "wakeup_count", "type": ["int", "null"]},
        {"name": "temperature",  "type": ["float", "null"]},
        {"name": "pressure", "type": ["float", "null"]},
        {"name": "humidity", "type": ["float", "null"]},
        {"name": "battery", "type": ["float", "null"]},
        {"name": "soil", "type": ["float", "null"]}
    ]
}'''

schema = avro.schema.parse(avro_schema)

admin = KafkaAdminClient(bootstrap_servers = broker, client_id = client_id)
producer = KafkaProducer(bootstrap_servers = broker, client_id = client_id)

topics = admin.list_topics()
#print(topics)

if not msensor1_topic in topics:
    topic_list = []
    topic_list.append(NewTopic(name = msensor1_topic, num_partitions = 1, replication_factor = 1))
    admin.create_topics(new_topics = topic_list, validate_only = False)

'''
Sending data to Kafka server in Avro format
'''

async def sendData(producer, topic, data, schema):
    if data != None and len(data):
        try:
            bytes_writer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_writer)
            nCnt = np.frombuffer(data, count=1, dtype=np.int32)[0]
            fNotify = np.frombuffer(data, offset=4, dtype=np.float32)

            d = datetime.datetime.now()
            ts = d.timestamp()
            x = {
                "timestamp": ts, 
                "wakeup_count": int(nCnt), 
                "temperature": float(fNotify[0]), 
                "pressure": float(fNotify[1]), 
                "humidity": float(fNotify[2]), 
                "battery": float(fNotify[3]), 
                "soil": float(fNotify[4])
                }
            writer = DatumWriter(schema)
            writer.write(datum=x, encoder=encoder)
            raw_bytes = bytes_writer.getvalue()
            producer.send(topic = topic, value = raw_bytes)
        except Exception as e: # work on python 3.x
            print('Failed: %s' % e)

async def printData(data):
    if data != None and len(data):
        try:
            nCnt: int = np.frombuffer(data, count=1, dtype=np.int32)[0]
            fNotify: float = np.frombuffer(data, offset=4, dtype=np.float32)
            print(f"  Date/Time: {datetime.datetime.now()}")
            print(f" Boot Count: {nCnt}")
            print(f"Temperature: {fNotify[0]:.1f} °C")
            print(f"   Pressure: {fNotify[1]:.0f} Pa")
            print(f"   Humidity: {fNotify[2]:.1f} %")
            print(f"    Battery: {fNotify[3]:.2f} V")
            print(f"       Soil: {fNotify[4]:.1f} %")
        except Exception as e: # work on python 3.x
            print('Failed: %s' % e)

def t_callback(sender: BleakGATTCharacteristic, data: bytearray):
    printData(data)

async def main(producer, topic, schema):
    while True:
        address = ['A0:B7:65:59:6F:BA']
        '''
        devices = []
        try:
            # Scan is required to ensure stable reconnecion to device, as per Bleak manual
            print("Scan for BLE devices")
            devices = await BleakScanner.discover()
        except:
            print("BLE scanner failed")
            pass

        if (len(devices)):
            for d in devices:
                print(d)
    #            print(d.name)
    #            print(d.address)
                if d.name == 'W55':
                    print('Found W55!')
                    address.append(d.address) #'A0:B7:65:59:6F:BA'
        '''
        
        if len(address):
            for a in address:
                try:
                    ble = BleakClient(a)
                    async with ble as client:
                        try:
                            print("Connected")

                            if (not client.is_connected):
                                print("Connection failed")
                                raise "client not connected"
                            '''
                            services = await client.get_services()
                            for s in services:
                                print(s)
                                for c in s.characteristics:
                                    print(c)
                            '''
                            await asyncio.sleep(1)
                            data = await client.read_gatt_char(t_uuid)

                            sleepInterval = 30*60;
                            read = await client.read_gatt_char(sleep_uuid)
                            nInterval: int = np.frombuffer(read, count=1, dtype=np.int32)[0]
                            await client.write_gatt_char(sleep_uuid, sleepInterval.to_bytes(4, "little"))
    #                        await client.start_notify(t_uuid, t_callback)
    #                        print("Wait for notification")
                            await sendData(producer=producer, topic=topic, data=data, schema=schema)
                            await printData(data=data)
                            print(f"Old Sleep Interval: {nInterval}")
                            print(f"New Sleep Interval: {sleepInterval}")

                            await asyncio.sleep(15) # not too often
                #                        print("Stop notification") 
                #                        await client.stop_notify(t_uuid)
                            print("Disconnect")
                            await client.disconnect()
                        except Exception as e: # work on python 3.x
                            print('Failed: %s' % e)

                except:
                    pass # Waiting for sensor to wakeup and go online. Not a error.

#                except Exception as e: # work on python 3.x
#                    print('Failed: %s' % e)

        await asyncio.sleep(1)

#asyncio.run()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(producer=producer, topic=msensor1_topic, schema=schema))