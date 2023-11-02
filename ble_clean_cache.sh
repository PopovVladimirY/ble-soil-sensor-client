#!/bin/sh

# During development, when device description changes often, there are possible
# confilcts with cached device data. Clean it up to restore operation.

bluetoothctl -- remove A0:B7:65:59:6F:BA
bluetoothctl -- remove A0:B7:65:67:FE:26

#prior to BlueZ 5.62 you also need to manually delete the GATT cache**
sudo rm "/var/lib/bluetooth/DC:A6:32:54:0C:97/cache/A0:B7:65:59:6F:BA"
sudo rm "/var/lib/bluetooth/DC:A6:32:54:0C:97/cache/A0:B7:65:67:FE:26"

