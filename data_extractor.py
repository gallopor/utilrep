import os
import json
from velocity.velsession import VelSession
from velocity.inventory import Inventory
from velocity.reservation import Reservation

from settings import DATA_DIR, VELOCITY_HOST, VELOCITY_USER, VELOCITY_PSWD, \
                     START_DATE, END_DATE

obj_vs = VelSession(host=VELOCITY_HOST, user=VELOCITY_USER, pswd=VELOCITY_PSWD)
obj_inv = Inventory(obj_vs)
obj_rsv = Reservation(obj_vs)

# devices = obj_inv.get_devices()
# fp = open(os.path.join(DATA_DIR, 'devices.json'), 'w+')
# json.dump(devices, fp, indent=4)
# fp.close()
# 
# ports = obj_inv.get_ports()
# fp = open(os.path.join(DATA_DIR, 'ports.json'), 'w+')
# json.dump(ports, fp, indent=4)
# fp.close()

template = 'Spirent Test Center'
template_id = obj_inv.query_template_id(template)
print(template_id)
util_rep = obj_rsv.get_util_by_template(template_id, START_DATE, END_DATE)
fp = open(os.path.join(DATA_DIR, 'utilization.json'), 'w+')
json.dump(util_rep, fp, indent=4)
fp.close()
    