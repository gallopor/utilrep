import time
from velocity.velcaller import VelCaller


class Utilization(VelCaller):

    def __init__(self, vs, version='v6'):
        super(Utilization, self).__init__(vs)
        
        self.version = version
        self.prefix = '/velocity/api/reservation/' + version
        
    def get_util_report(self):
        url = self.prefix + '/reports'
        return self.vget(url)
    
    def get_util_by_template(self, template_id, start, end):
        ts_sd = int(time.mktime(time.strptime(start, '%Y-%m-%d')) * 1000)
        ts_ed = int(time.mktime(time.strptime(end, '%Y-%m-%d')) * 1000)
        
        url = self.prefix + '/templates/' + template_id + '/utilization'
        params = {
            'startDate': str(ts_sd),
            'endDate': str(ts_ed)
        }
        util_tplt = self.vget(url, **params)
        return util_tplt

    def get_util_by_device(self, start, end):
        ts_sd = int(time.mktime(time.strptime(start, '%Y-%m-%d')) * 1000)
        ts_ed = int(time.mktime(time.strptime(end, '%Y-%m-%d')) * 1000)

        url = self.prefix + '/reports'
        total = None
        count = 0
        offset = 0
        util_device = {}
        while total is None or count < total:
            params = {
                'offset': str(offset),
                'startAfter': str(ts_sd),
                'endBefore': str(ts_ed),
            }
            ret = self.vget(url, **params)
            print(ret)
            total = ret['total']
            count = count + ret['count']
            offset = count

            for device in ret['reports']:
                new = {}
                new['name'] = device['device']['name']
                new['utilization'] = device['utilization']['period']
                util_device[device['device']['id']] = new
        return util_device

    def get_util_by_user(self, start, end, type='TOTAL_HOURS'):
        ts_sd = int(time.mktime(time.strptime(start, '%Y-%m-%d')) * 1000)
        ts_ed = int(time.mktime(time.strptime(end, '%Y-%m-%d')) * 1000)

        url = self.prefix + '/reports'
        total = None
        count = 0
        offset = 0
        util_user = {}
        while total is None or count < total:
            params = {
                'offset': str(offset),
                'reportType': 'USER',
                'measure': type,
                'startAfter': str(ts_sd),
                'endBefore': str(ts_ed)
            }
            ret = self.vget(url, **params)
            total = ret['total']
            count = count + ret['count']
            offset = count

            for user in ret['reports']:
                new = {}
                new['name'] = user['user']['name']
                new['utilization'] = user['utilization']['period']
                util_user[user['user']['id']] = new
        return util_user

        
if __name__ == "__main__":
    from velocity.velsession import VelSession
    from velocity.inventory import Inventory
    import os
    import json
    from settings import DATA_DIR
    
    vs = VelSession(host='10.190.15.229', user='jxie', pswd='Spirent-101')
#    vs = VelSession(host='192.168.1.21', user='jxie', pswd='Spirent-101')
#    vs = VelSession(host='192.168.3.51', user='jxie', pswd='Spirent-101')
    vel_util = Utilization(vs)
    vel_inv = Inventory(vs)

    start = '2018-01-01'
    end = '2018-01-31'
#    ret = vel_util.get_util_by_user('TOTAL_HOURS', start, end)
    ret = vel_util.get_util_by_device(start, end)
    print(ret)

#    fn = 'util_user.json'
    fn = 'util_device.json'
    fp = open(os.path.join(DATA_DIR, fn), 'w+')
    json.dump(ret, fp, indent=4)
    fp.close()

#     ret = resv.query_resv_in_period('STCvPair', 1483200000000, 1507564800000)
#     print(ret)
#     rep = resv.get_util_report()
#     print(rep)
#     url = resv.prefix + '/reports'
#     response_info = resv.vget(url, reportType='USER', periodType='PAST', measure='TOTAL_HOURS')
#     print(response_info)
    

    
    
    
