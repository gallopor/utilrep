import os
import json

from elasticsearch import Elasticsearch, helpers
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.filterwarnings('ignore', 'Connecting to')

from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, \
                     ELASTICSEARCH_USER, ELASTICSEARCH_PSWD
from settings import DATA_DIR

''' 读取devices数据 '''
dfp = open(os.path.join(DATA_DIR, 'devices.json'), 'r')
devices = json.load(dfp)
dfp.close()
''' 读取ports数据 '''
pfp = open(os.path.join(DATA_DIR, 'ports.json'), 'r')
ports = json.load(pfp)
pfp.close()

es = Elasticsearch(host=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT, \
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PSWD), \
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
   
if (len(actions) > 0):
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
    
if (len(actions) > 0):
    helpers.bulk(es, actions)
    print('Ports have been imported. Total number: ' + str(len(actions)))
    del actions[0:len(actions)]    
        