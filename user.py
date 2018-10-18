import os
import json
import datetime

from velocity.velsession import VelSession
from velocity.inventory import Inventory
from velocity.utiliation import Utilization

from elasticsearch import Elasticsearch, helpers
import urllib3
import warnings

from settings import START_DATE
from settings import DATA_DIR
from settings import VELOCITY_HOST, VELOCITY_USER, VELOCITY_PSWD
from settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, \
    ELASTICSEARCH_USER, ELASTICSEARCH_PSWD

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', 'Connecting to')


vs = VelSession(host=VELOCITY_HOST, user=VELOCITY_USER, pswd=VELOCITY_PSWD)
vel_inv = Inventory(vs)
vel_util = Utilization(vs)

es = Elasticsearch(host=ELASTICSEARCH_HOST, port=ELASTICSEARCH_PORT,
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PSWD),
                   use_ssl=True, verify_certs=False)

''' 创建elasticsearch索引 '''
util_user_mapping = {
    'mappings': {
        'util_user': {
            'properties': {
                'name': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'utilization': {
                    'type': 'double'
                },
                'date': {
                    'tpye': 'date',
                    'format': 'epoch_millis'
                }
            }
        }
    }
}
if not es.indices.exists('util_user'):
    es.indices.create(index='util_user', body=json.dumps(util_user_mapping))

''' 加载更新记录文件 '''
with open(os.path.join(DATA_DIR, 'user_log.json'), 'r') as fp:
    update_log = json.load(fp)
    last_date = update_log['last_date']

''' 根据更新记录确定本次更新的起止点日期（左闭右开）'''
today = datetime.datetime.now().date()
if last_date == 0:
    if START_DATE is None:
        begin = today - datetime.timedelta(days=1)
    else:
        begin = datetime.datetime.strptime(START_DATE, '%Y-%m-%d').date()
else:
    begin = datetime.date.fromtimestamp(last_date)

for i in range((today - begin).days):
    sd = begin + datetime.timedelta(days=i)
    ed = sd + datetime.timedelta(days=1)
    util_user = vel_util.get_util_by_user(str(sd), str(ed))

    ts = datetime.datetime.combine(sd, datetime.time.min).timestamp()
    actions = []
    for user in util_user:
        util = util_user[user]
        util['date'] = int(ts) * 1000
#        print(json.dumps(util))
        action = {
            "_index": 'util_user',
            "_type": 'daily',
            "_request_timeout": 1000,
            "_source": json.dumps(util)
        }
        actions.append(action)

    if len(actions) > 0:
        helpers.bulk(es, actions)
        print('User daily utilization have been imported. Date: ' + str(sd))
        del actions[0:len(actions)]

''' 保存更新记录 '''
with open(os.path.join(DATA_DIR, 'user_log.json'), 'w') as fp:
    update_log['last_date'] = str(ed)
    json.dump(update_log, fp)

