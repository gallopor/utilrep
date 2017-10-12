import json
from velsession import VelSession
from inventory import Inventory

from elasticsearch import Elasticsearch, helpers
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.filterwarnings('ignore', 'Connecting to')

VELOCITY_HOST = '192.168.1.21'
VELOCITY_USER = 'jimmy'
VELOCITY_PSWD = 'Spirent'

ELASTICSEARCH_HOST = '192.168.1.20'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USER = 'api'
ELASTICSEARCH_PSWD = 'index'

vs = VelSession(host=VELOCITY_HOST, user=VELOCITY_USER, pswd=VELOCITY_PSWD)
inv = Inventory(vs)

devices = inv.get_devices()
ports = inv.get_ports()

es = Elasticsearch(host=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT, \
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PSWD), \
                   use_ssl=True, verify_certs=False)

es.indices.create(index='inventory')

j = 0
actions = []
for d_id in devices:
    action = {
        "_index": "inventory",
        "_type": "device",
        "_id": j + 1,
        "_source": json.dumps(devices[d_id])
    }
    actions.append(action)
    j += 1
 
    if (len(actions) == 1000):
        helpers.bulk(es, actions)
        del actions[0:len(actions)]

if (len(actions) > 0):
    helpers.bulk(es, actions)
    del actions[0:len(actions)]
    
for p_id in ports:
    action = {
        "_index": "inventory",
        "_type": "port",
        "_id": j + 1,
        "_source": json.dumps(ports[p_id])
    }
    actions.append(action)
    j += 1
  
    if (len(actions) == 1000):
        helpers.bulk(es, actions)
        del actions[0:len(actions)]
  
if (len(actions) > 0):
    helpers.bulk(es, actions)
    del actions[0:len(actions)]    
    
    