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

es = Elasticsearch(host=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT, \
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PSWD), \
                   use_ssl=True, verify_certs=False)

 
if es.indices.exists('utilization'):
    es.indices.delete('utilization')
    
fp = open(os.path.join(DATA_DIR, 'utilization.json'), 'r')
utilizations = json.load(fp)['report']
fp.close()
 
utilization_mapping = {
    'mappings': {
        'Spirent TestCenter': {
            'properties': {
                'date': {
                  'type': 'date',
                  'format': 'epoch_millis'
                },
                'utilization': {
                    'type': 'double'
                }
            }
        }
    }    
}
 
es.indices.create(index='utilization', body=json.dumps(utilization_mapping))
 
actions = []
for j in range(len(utilizations)):
    action = {
        "_index": "utilization",
        "_type": "Spirent TestCenter",
        "_id": j + 1,
        "_request_timeout": 1000,
        "_source": json.dumps(utilizations[j])
    }
    actions.append(action)
      
if (len(actions) > 0):
    helpers.bulk(es, actions)
    print('Utilization have been imported. Total number: ' + str(len(actions)))
    del actions[0:len(actions)]    
    
    