import json
import requests
from requests.auth import HTTPBasicAuth

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VelSession():

    def __init__(self, host, **params):
        
        self.base_url = 'https://' + host
        self.headers = {'X-Auth-Token': '', 'Content-type': 'application/json'}
        
        if 'token' in params:
            self.headers['X-Auth-Token'] = params['token']
        else:
            auth_url = 'https://' + host + '/velocity/api/auth/v1/token'
            response = requests.get(auth_url, \
                        auth=HTTPBasicAuth(params['user'], params['pswd']), \
                        verify=False)
        
            if response.status_code == 200:
                response2dict = json.loads(response.text)
                self.headers['X-Auth-Token'] = response2dict['token']

    def get(self, url):
        return requests.get(url, headers=self.headers, verify=False)

    def post(self, url, body):
        '''Tranform dict to json string, then Velocity can parse successfully.'''
        jstr = json.dumps(body)
        r = requests.post(url, headers=self.headers, data=jstr, verify=False)
        if(len(r.text) > 0):
            return json.loads(r.text)
        
    def token(self):
        return self.headers['X-Auth-Token']

if __name__ == "__main__":
    vs1 = VelSession('192.168.1.21', user='jimmy', pswd='Spirent')
    token = vs1.token()
    print(token)
    
