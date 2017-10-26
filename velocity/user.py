from velcaller import VelCaller

class User(VelCaller):
    
    def __init__(self, vs, version='v7'):
        super(User, self).__init__(vs)
        
        self.version = version
        self.prefix = '/velocity/api/user/' + version
        self.users = None

    def get_users(self):
        url = self.prefix + '/profiles'
        response_info = self.vget(url)

        total = None
        count = 0
        offset = 0
        users = {}
        while total is None or count < total:
            response_info = self.vget(url, offset=str(offset))
            total = response_info['total']
            count = count + response_info['count']
            offset = count
             
            for user in response_info['profiles']:
                new = {}
                for key in ['name', 'login', 'role', 'groups']:
                    new[key] = user[key]
                users[user['id']] = new
 
        self.users = users
        return users
    
    def get_current_user(self):
        url = self.prefix + '/profile/current'
        user = self.vget(url)
        return user['id']

if __name__ == "__main__":
    from velsession import VelSession

    vs = VelSession(host='192.168.3.51', user='jimmy', pswd='Spirent')
    uprof = User(vs)

    users = uprof.get_users()
    print(users)
    
    u_id = uprof.get_current_user()
    print(uprof.users[u_id])
    
    
    