import asyncio
import sys
import numpy as np
import datetime 
#import bleak
from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic

def printData(data):
    if data != None and len(data):
        fNotify: float = np.frombuffer(data, dtype=np.float32)
        print(f"  Date/Time: {datetime.datetime.now()}")
        print(f"Temperature: {fNotify[0]:.1f} °C")
        print(f"   Pressure: {fNotify[1]:.0f} Pa")
        print(f"   Humidity: {fNotify[2]:.1f} %")
        print(f"    Battery: {fNotify[3]:.2f} V")
        print(f"       Soil: {fNotify[4]:.1f} %")

def t_callback(sender: BleakGATTCharacteristic, data: bytearray):
    printData(data)

t_uuid: str = '9b5099ae-10f0-4a78-a8b7-eb086e3cb69b'

async def main():
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
#                    address.append(d.address) #'A0:B7:65:59:6F:BA'
                            
        '''
        if len(address):
            for a in address:
                try:
                    ble = BleakClient(a)
                    async with ble as client:
                        print("Connected")

                        if (not client.is_connected):
                            print("Connection failed")
                            raise "client not connected"

                        await asyncio.sleep(1)
                        data = await client.read_gatt_char(t_uuid)
                        printData(data)
#                        await client.start_notify(t_uuid, t_callback)
#                        print("Wait for notification")
                        await asyncio.sleep(15)
            #                        print("Stop notification") 
            #                        await client.stop_notify(t_uuid)
                        print("Disconnect")
                        await client.disconnect()
                except:
                    pass

        await asyncio.sleep(1)

asyncio.run(main())
