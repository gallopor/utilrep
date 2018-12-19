import time
from velocity.velcaller import VelCaller


class License(VelCaller):

    def __init__(self, vs, version='v3'):
        super(License, self).__init__(vs)
        
        self.version = version
        self.prefix = '/velocity/api/license/' + version
        
    def get_lic_usage(self, start, end):
        ts_sd = int(time.mktime(time.strptime(start, '%Y-%m-%d')) * 1000)
        ts_ed = int(time.mktime(time.strptime(end, '%Y-%m-%d')) * 1000)

        url = self.prefix + '/audit'
        total = None
        count = 0
        offset = 0
        lic_usage = {}
        while total is None or count < total:
            params = {
                'offset': str(offset),
                'startAfter': str(ts_sd),
                'endBefore': str(ts_ed),
            }
            ret = self.vget(url, **params)
            total = ret['total']
            count = count + ret['count']
            offset = count

            for item in ret['items']:
                lic_usage[item['userId']] = item
        return lic_usage


if __name__ == "__main__":
    from velocity.velsession import VelSession

#    vs = VelSession(host='10.190.15.229', user='jxie', pswd='Spirent-101')
    vs = VelSession(host='192.168.1.21', user='jxie', pswd='Spirent-101')
#    vs = VelSession(host='192.168.3.51', user='jxie', pswd='Spirent-101')
    vel_lic = License(vs)

    start = '2018-11-01'
    end = '2018-12-31'
    ret = vel_lic.get_lic_usage(start, end)
    print(ret)



    
    
    
