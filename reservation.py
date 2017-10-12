import time
from velcaller import VelCaller

class Reservation(VelCaller):

    def __init__(self, vs, version='v7'):
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
        
        

    def getTopoIdByName(self, name):    
        url = '/velocity/api/topology/v4/topologies'
        tp_f = 'name::' + name
        tp_info = self.vget(url, filter=tp_f)
        tp_id = tp_info['topologies'][0]['id']
        return tp_id
 
          
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
    
    def get_resv_in_period(self, tp_name, start, end='now'):
        tp_id = self.getTopoIdByName(tp_name)
        dp = {
            'filter': 'topologyId::' + tp_id, 
            'startAfter': str(start), 
            'endBefore': str(end), 
            'sortBy': 'created'
        }
        url = '/velocity/api/reservation/v6/reservations/' 
        return self.vget(url, **dp)
        
if __name__ == "__main__":
    from velsession import VelSession

    vs = VelSession(host='192.168.1.21', user='daemon', pswd='Spirent')
    resv = Reservation(vs)

