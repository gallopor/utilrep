import os
import json

from elasticsearch import Elasticsearch, helpers
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.filterwarnings('ignore', 'Connecting to')

from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, \
                     ELASTICSEARCH_USER, ELASTICSEARCH_PSWD, DATA_DIR

es = Elasticsearch(host=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT, \
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PSWD), \
                   use_ssl=True, verify_certs=False)

fp = open(os.path.join(DATA_DIR, 'devices.json'), 'r')
devices = json.load(fp)
fp.close()
 
fp = open(os.path.join(DATA_DIR, 'ports.json'), 'r')
ports = json.load(fp)
fp.close()
 
# inventory_mapping = {
#     "mappings": {
#         "device": {
#             "properties": {
#                 "name": {
#                   "type": "date",
#                   "format": "epoch_millis"
#                 },
#                 "utilization": {
#                     "type": "double"
#                 }
#             }
#         }
#     }    
# } 
#  
# es.indices.create(index='inventory')
#  
# j = 1
# actions = []
# for d_id in devices:
#     action = {
#         "_index": "inventory",
#         "_type": "device",
#         "_id": j,
#         "_source": json.dumps(devices[d_id])
#     }
#     actions.append(action)
#     j += 1
#   
# if (len(actions) > 0):
#     helpers.bulk(es, actions)
#     print('Devices have been imported. Total number: ' + str(len(actions)))
#     del actions[0:len(actions)]
#      
# for p_id in ports:
#     action = {
#         "_index": "inventory",
#         "_type": "port",
#         "_id": j,
#         "_request_timeout": 1000,
#         "_source": json.dumps(ports[p_id])
#     }
#     actions.append(action)
#     j += 1
#    
# if (len(actions) > 0):
#     helpers.bulk(es, actions)
#     print('Ports have been imported. Total number: ' + str(len(actions)))
#     del actions[0:len(actions)]    
#      
fp = open(os.path.join(DATA_DIR, 'utilization.json'), 'r')
util_rep = json.load(fp)
utilizations = util_rep['report']
fp.close()
 
utilization_mapping = {
    "mappings": {
        "Spirent Test Center": {
            "properties": {
                "date": {
                  "type": "date",
                  "format": "epoch_millis"
                },
                "utilization": {
                    "type": "double"
                }
            }
        }
    }    
}
 
es.indices.create(index='utilization', body=utilization_mapping)
 
actions = []
for j in range(len(utilizations)):
    action = {
        "_index": "utilization",
        "_type": "Spirent Test Center",
        "_id": j + 1,
        "_request_timeout": 1000,
        "_source": json.dumps(utilizations[j])
    }
    actions.append(action)
      
if (len(actions) > 0):
    helpers.bulk(es, actions)
    print('Utilization have been imported. Total number: ' + str(len(actions)))
    del actions[0:len(actions)]
     
    
    
    