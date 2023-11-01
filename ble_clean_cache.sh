#!/bin/sh

bluetoothctl -- remove A0:B7:65:59:6F:BA

#prior to BlueZ 5.62 you also need to manually delete the GATT cache**
sudo rm "/var/lib/bluetooth/DC:A6:32:54:0C:97/cache/A0:B7:65:59:6F:BA"