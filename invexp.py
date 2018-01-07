import os
import json
from velocity.velsession import VelSession
from velocity.inventory import Inventory
from velocity.reservation import Reservation

from settings import DATA_DIR, VELOCITY_HOST, VELOCITY_USER, VELOCITY_PSWD

vs = VelSession(host=VELOCITY_HOST, user=VELOCITY_USER, pswd=VELOCITY_PSWD)
vel_inv = Inventory(vs)
vel_rsv = Reservation(vs)

devices = vel_inv.get_devices()
fp = open(os.path.join(DATA_DIR, 'devices.json'), 'w+')
json.dump(devices, fp, indent=4)
fp.close()
 
ports = vel_inv.get_ports()
fp = open(os.path.join(DATA_DIR, 'ports.json'), 'w+')
json.dump(ports, fp, indent=4)
fp.close()
    