import asyncio
import sys
import numpy as np
import datetime 
from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic

def t_callback(sender: BleakGATTCharacteristic, data: bytearray):
    value: float = np.frombuffer(data, dtype=np.float32)[0]
    t = datetime.datetime.now()
    print(f"Temperature: {value:.1f} ℃   at {t}")

def p_callback(sender: BleakGATTCharacteristic, data: bytearray):
    value: float = np.frombuffer(data, dtype=np.float32)[0]
    t = datetime.datetime.now()
    print(f"   Pressure: {value:.0f} Pa   at {t}")

def h_callback(sender: BleakGATTCharacteristic, data: bytearray):
    value: float = np.frombuffer(data, dtype=np.float32)[0]
    t = datetime.datetime.now()
    print(f"   Humidity: {value:.1f} %   at {t}")

def b_callback(sender: BleakGATTCharacteristic, data: bytearray):
    value: float = np.frombuffer(data, dtype=np.float32)[0]
    t = datetime.datetime.now()
    print(f"    Battery: {value:.2f} V   at {t}")

def m_callback(sender: BleakGATTCharacteristic, data: bytearray):
    value: float = np.frombuffer(data, dtype=np.float32)[0]
    t = datetime.datetime.now()
    print(f"       Soil: {value:.1f} %   at {t}")

t_uuid: str = '9b5099ae-10f0-4a78-a8b7-eb086e3cb69b'
p_uuid: str = 'd2bc7047-ef44-4c5f-9913-3ee6a174e44a'
h_uuid: str = '1c383a81-5387-41bc-b55f-3ff410da6f7e'
b_uuid: str = '2af553d1-3f9f-4b19-ac6c-82ced3255cd0'
m_uuid: str = 'ea936dd5-eafa-4f70-9b7a-6a794a4de3a9'

async def main():
    while True:
        try:
            devices = await BleakScanner.discover()
            for d in devices:
    #            print(d)
    #            print(d.name)
    #            print(d.address)
                if d.name == 'W55':
                    print('Found W55!')
                    address = d.address

                    try:
                        print("Connect")
                        async with BleakClient(address) as client:

                            if (not client.is_connected):
                                raise "client not connected"

    #                        services = await client.get_services()

    #                        for service in services:
    #                            print('service', service.handle, service.uuid, service.description)

                            print("Start notification")
                            await client.start_notify(t_uuid, t_callback)
                            await client.start_notify(p_uuid, p_callback)
                            await client.start_notify(h_uuid, h_callback)
                            await client.start_notify(b_uuid, b_callback)
                            await client.start_notify(m_uuid, m_callback)
                            print("Wait for notification")
                            await asyncio.sleep(20)
    #                        print("Stop notification") 
    #                        await client.stop_notify(t_uuid)
    #                        await client.stop_notify(p_uuid)
    #                        await client.stop_notify(h_uuid)
    #                        await client.stop_notify(b_uuid)
    #                        await client.stop_notify(m_uuid)
                            print("Disconnect")
                            await client.disconnect()
                            await asyncio.sleep(1)
                    except:
                        await asyncio.sleep(1)
                        pass
        except:
            pass

asyncio.run(main())
