import json

from velocity.velsession import VelSession
from velocity.inventory import Inventory
from velocity.reservation import Reservation

from elasticsearch import Elasticsearch, helpers
import urllib3
import warnings

from settings import VELOCITY_HOST, VELOCITY_USER, VELOCITY_PSWD
from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, \
    ELASTICSEARCH_USER, ELASTICSEARCH_PSWD

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', 'Connecting to')

'''从Velocity里获取设备及端口数据'''
vs = VelSession(host=VELOCITY_HOST, user=VELOCITY_USER, pswd=VELOCITY_PSWD)
vel_inv = Inventory(vs)
vel_rsv = Reservation(vs)

devices = vel_inv.get_devices()
ports = vel_inv.get_ports()

'''将设备及端口数据导入Elasticsearch'''
es = Elasticsearch(host=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT,
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PSWD),
                   use_ssl=True, verify_certs=False)

if es.indices.exists('inventory'):
    es.indices.delete('inventory')

doc = {
    'mappings': {
        'devices': {
            'properties': {
                'template': {
                    'type': 'string',
                    'index': 'not_analyzed',
                },
            }
        }
    }
}
es.indices.create(index='inventory', body=json.dumps(doc))

j = 1
actions = []
for d_id in devices:
    action = {
        "_index": "inventory",
        "_type": "device",
        "_id": j,
        "_source": json.dumps(devices[d_id])
    }
    actions.append(action)
    j += 1

if len(actions) > 0:
    helpers.bulk(es, actions)
    print('Devices have been imported. Total number: ' + str(len(actions)))
    del actions[0:len(actions)]

for p_id in ports:
    action = {
        "_index": "inventory",
        "_type": "port",
        "_id": j,
        "_request_timeout": 1000,
        "_source": json.dumps(ports[p_id])
    }
    actions.append(action)
    j += 1

if len(actions) > 0:
    helpers.bulk(es, actions)
    print('Ports have been imported. Total number: ' + str(len(actions)))
    del actions[0:len(actions)]


