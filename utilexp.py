import os
import json
from velocity.velsession import VelSession
from velocity.inventory import Inventory
from velocity.reservation import Reservation

from settings import DATA_DIR, VELOCITY_HOST, VELOCITY_USER, VELOCITY_PSWD
from settings import START_DATE, END_DATE

vs = VelSession(host=VELOCITY_HOST, user=VELOCITY_USER, pswd=VELOCITY_PSWD)
vel_inv = Inventory(vs)
vel_rsv = Reservation(vs)

template = 'Spirent Test Center'
template_id = vel_inv.query_template_id(template)
#print(template_id)
util_rep = vel_rsv.get_util_by_template(template_id, START_DATE, END_DATE)
fp = open(os.path.join(DATA_DIR, 'utilization.json'), 'w+')
json.dump(util_rep, fp, indent=4)
fp.close()
    