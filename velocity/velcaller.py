import json
from velocity.velsession import VelSession


class VelCaller:

    vsession = None

    def __init__(self, vs):
        self.vsession = vs

    def vget(self, url, **params):
        """
        params can be:
            sortBy - sorted by specific key.
            filter - filtered by specific key.
            other API related parameters
        """
        if self.vsession is not None:
            if len(params) > 0:
                url = self.vsession.base_url + url + '?'
                for key in params:
                    if isinstance(params[key], list):
                        p = '&'.join(params[key])
                    else:
                        p = params[key]
                    url = url + key + '=' + p + '&' 
                url = url.rstrip('&') 
            else:
                url = self.vsession.base_url + url
#            print(url)
            return json.loads(self.vsession.get(url).text)
            
    def vpost(self, url, body=None, **params):
        if self.vsession is not None:
            if len(params) > 0:
                url = self.vsession.base_url + url + '?'
                for key in params:
                    url = url + key + '=' + params[key] + '&' 
                url = url.rstrip('&') 
            else:
                url = self.vsession.base_url + url            

            return self.vsession.post(url, body)
        
    def vtime(self):
        url = '/velocity/api/util/v1/time'
        return self.vget(url)


if __name__ == "__main__":
    vs = VelSession(host='192.168.1.21', user='jimmy', pswd='Spirent')
    vc = VelCaller(vs)
    print(vc.vtime())
