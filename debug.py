import json

from elasticsearch import Elasticsearch, helpers
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.filterwarnings('ignore', 'Connecting to')

ELASTICSEARCH_HOST = '192.168.1.20'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USER = 'api'
ELASTICSEARCH_PSWD = 'index'

es = Elasticsearch(host=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT, \
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PSWD), \
                   use_ssl=True, verify_certs=False)

#es.indices.create(index='library')

id = 1
body = {'name': 'book1', 'author': {'first': 'jing', 'last': 'xie'}, 'price': 100}
es.index(index='library', doc_type='books', id=id, body=json.dumps(body))  