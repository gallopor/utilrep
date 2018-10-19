import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# VELOCITY_HOST = '192.168.1.21'
# VELOCITY_USER = 'jimmy'
# VELOCITY_PSWD = 'Spirent'
VELOCITY_HOST = '172.31.234.241'
VELOCITY_USER = 'jxie'
VELOCITY_PSWD = 'Spirent-101'

ELASTICSEARCH_HOST = '172.31.234.242'
# ELASTICSEARCH_HOST = '192.168.1.20'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USER = 'api'
ELASTICSEARCH_PSWD = 'index'

START_DATE = '2018-09-16'

TEMPLATES = ['Server']
# TEMPLATES = ['Instrument_stc',
#              'Instrument_ixia',
#              'FH_SWITCH_4820',
#              'FH_SWITCH_5800',
#              'FH_SWITCH_7800',
#              'Citrans_R640',
#              'Citrans_R810',
#              'Citrans_R845',
#              'Citrans_R860',
#              'Citrans_R865',
#              'Citrans_R8000-3',
#              'Citrans_R8000-5',
#              'Citrans_R8000-10',
#              'Citrans_R820v2',
#              'Citrans_R830E',
#              'Citrans_R835E',
#              'Citrans_R835Ev3',
#              'Citrans_PTN_620',
#              'Citrans_PTN_640',
#              'Citrans_PTN_660',
#              'Citrans_PTN_680',
#              'Citrans_PTN_650_U2',
#              'Citrans_PTN_650_U3',
#              'Citrans_PTN_650_U5',
#              'Citrans_PTN_690_U10',
#              'Citrans_PTN_690_U20',
#              'Citrans_PTN_690_U30']

