import time
from velocity.velcaller import VelCaller


class Reservation(VelCaller):

    def __init__(self, vs, version='v6'):
        super(Reservation, self).__init__(vs)
        
        self.version = version
        self.prefix = '/velocity/api/reservation/' + version
        
        ''' 'description' can not be None. I don't know why?'''
        self.reservation_body = {
            'name': None,
            'description': '',
            'start': None,
            'end': None,
            'duration': None,
            'topologyId': None,
            'topologyVersionId': None,
            'cloudId': None,
            'isRecurrent': None,
            'recurrence': None,
            'resources': None,
            'intervalToRunEndTestCase': None,
            'startTestCases': None,
            'endTestCases': None,
            'request': None,
            'notes': None,
            'attendees': None,
            'resolution': None,
            'customConditions': None,
            'customUtilizations': None,
            'customLinkConditions': None,
            'workOrder': None
        } 
        
    def getActResvByTopo(self, tp_name):
        tp_id = self.getTopoIdByName(tp_name)
        
        url = '/velocity/api/reservation/v6/reservations/' 
        vfilter = ['status::ACTIVE', 'topologyId::' + tp_id]
        return self.vget(url, filter=vfilter)
    
    def getActResvByMe(self):
        user = self.vget('/velocity/api/user/v6/profile/current')
        user_id = user['id']
    
        url = '/velocity/api/reservation/v6/reservations/' 
        vfilter = ['status::ACTIVE', 'creatorId ::' + user_id]
        return self.vget(url, filter=vfilter)

    def topo_reserve(self, name, duration):
        ''' reservation's name is topology's name plus current time stamp. '''
        tp_id = self.query_topo_id_by_name(name)
        ts = time.strftime("%Y%m%d%H%M%S")
        resv_name = name + '-' + ts
        self.reservation_body['name'] = resv_name
        self.reservation_body['duration'] = duration
        self.reservation_body['topologyId'] = tp_id
        
        url = self.prefix + '/reservation'
        resv_info = self.vpost(url, self.reservation_body)
        self.last_reservation = resv_info
        return resv_info

    def topo_release(self, resv_id=None):
        if(resv_id == None):
            if (self.last_reservation != None):
                resv_id = self.last_reservation['id']
        url = self.prefix + '/reservation' + resv_id + '/action?type=cancel'
        return self.vpost(url)
    
    def query_topo_id_by_name(self, name):    
        url = '/velocity/api/topology/v4/topologies'

        tp_f = 'name::' + name
        tp_info = self.vget(url, filter=tp_f)
        tp_id = tp_info['topologies'][0]['id']
        return tp_id
 
    def query_resv_in_period(self, tp_name, start, end='now'):
        tp_id = self.query_topo_id_by_name(tp_name)
        dp = {
            'filter': 'topologyId::' + tp_id, 
            'startAfter': str(start), 
            'endBefore': str(end), 
            'sortBy': 'created'
        }
        url = self.prefix + '/reservations'
        return self.vget(url, **dp)
    
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
        util_info = self.vget(url, **params)
        return util_info

    def get_util_by_user(self, type, start, end):
        # type = 'TOTAL_COUNT'
        # type = 'TOTAL_HOURS'
        ts_sd = int(time.mktime(time.strptime(start, '%Y-%m-%d')) * 1000)
        ts_ed = int(time.mktime(time.strptime(end, '%Y-%m-%d')) * 1000)

        url = self.prefix + '/reports'
        total = None
        count = 0
        offset = 0
        util_users = {}
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
                new['utiliation'] = user['utiliation']['period']
                util_users[user['id']] = new
        return util_users

        
if __name__ == "__main__":
    from velocity.velsession import VelSession
    from velocity.inventory import Inventory
    
#    vs = VelSession(host='10.190.15.229', user='jxie', pswd='Spirent-101')
#    vs = VelSession(host='192.168.1.21', user='jxie', pswd='Spirent-101')
    vs = VelSession(host='10.61.27.21', user='jxie', pswd='Spirent-101')
    vel_rsv = Reservation(vs)
    vel_inv = Inventory(vs)
    
#     ret = resv.query_resv_in_period('STCvPair', 1483200000000, 1507564800000)
#     print(ret)
#     rep = resv.get_util_report()
#     print(rep)
#     url = resv.prefix + '/reports'
#     response_info = resv.vget(url, reportType='USER', periodType='PAST', measure='TOTAL_HOURS')
#     print(response_info)
    
#     
#     start_date = '2017-01-01'
#     ts_start_date = str()
#     print(ts_start_date)
#     end_date = '2017-10-10'
#     ts_end_date = str(int(time.mktime(time.strptime(end_date, '%Y-%m-%d'))))
#     print(ts_end_date)
#     url = resv.prefix + '/templates/' + t_id + '/utilization?{' + ts_start_date + ',' + ts_end_date + '}'
#     
#     
#     url = '/velocity/api/reservation/v7/templates/2eab3479-eb97-4a0c-93b7-2d4d3dc4637a/utilization?startDate=1489334400000&endDate=1491408000000'   
#     
    template = 'STC_PORT'
    template_id = vel_inv.query_template_id(template)
    print(template_id)
    start_date = '2018-01-01'
    ts_start_date = int(time.mktime(time.strptime(start_date, '%Y-%m-%d')) * 1000)
    end_date = '2018-01-05'
    ts_end_date = int(time.mktime(time.strptime(end_date, '%Y-%m-%d')) * 1000)
    response_info = vel_rsv.get_util_by_template(template_id, start_date, end_date)
    print(response_info)
    
    
    
