from velocity.velcaller import VelCaller

class Inventory(VelCaller):
    
    def __init__(self, vs, version='v5'):
        super(Inventory, self).__init__(vs)
        
        self.version = version
        self.prefix = '/velocity/api/inventory/' + version
        self.categories = None
        self.devices = None

    def get_categories(self):
        url = self.prefix + '/templates'
        response_info = self.vget(url)
        
        '''提取templates有用信息，并将templates转化成字典'''
        templates = {}
        relation_map = {}
        for template in response_info['templates']:
            relation_map[template['id']] = template['parentId']   
            templates[template['id']] = template['name'].replace(' ', '')
        
        '''根据template之间的parent关系，设置category'''
        categories = {}
        for t_id in templates:
            parents = {}
            parent_id = t_id
            i = 0
            while parent_id is not None:
                parents['level' + str(i)] = templates[parent_id]
                parent_id = relation_map[parent_id]
                i += 1
            categories[t_id] = parents
            
        self.categories = categories
        return categories
    
    def get_devices(self):
        url = self.prefix + '/devices'
        
        if self.categories is None:
            self.get_categories()
            
        total = None
        count = 0
        offset = 0
        devices = {}
        while total is None or count < total:
            response_info = self.vget(url, offset=str(offset))
            total = response_info['total']
            count = count + response_info['count']
            offset = count
            
            for device in response_info['devices']:
                new = {}
                for key in ['name', 'isLocked', 'isOutOfService', 'interface', 'tags']:
                    new[key] = device[key]
                new['type'] = 'DEVICE'
                parents = self.categories[device['templateId']].copy()
                new['template'] = parents.pop('level0')
                new['parents'] = parents
                devices[device['id']] = new

        self.devices = devices
        return devices

    def get_ports(self):
        url = self.prefix + '/devices/ports'
        
        if self.devices is None:
            self.get_devices()
            
        total = None
        count = 0
        offset = 0
        ports = {}
        while total is None or count < total:
            response_info = self.vget(url, offset=str(offset))
            total = response_info['total']
            if response_info['count'] == 0:
                break
            count = count + response_info['count']
            offset = count
             
            for port in response_info['ports']:
                if port['name'] == 'uplink':
                    continue
                else:
                    new = {}
                    new['name'] = port['parentName'] + '::' + port['name']
                    new['type'] = 'PORT'
                    new['template'] = self.devices[port['parentId']]['template']
                    new['parents'] = self.devices[port['parentId']]['parents']
                    new['isLocked'] = port['isLocked']
                    ports[port['id']] = new

        self.ports = ports
        return ports

    def query_template_id(self, name):
        url = self.prefix + '/templates'

        tf = 'name::' + name
        response_info = self.vget(url, filter=tf)
        t_id = response_info['templates'][0]['id']
        return t_id

    def query_ports_by_template(self, template):
        t_id = self.get_template_id(template)
        
        url = self.prefix + '/devices/ports'
        pf = 'templateId::' + t_id
        return self.vget(url, filter=pf)

if __name__ == "__main__":
    from velocity.velsession import VelSession

#    vs = VelSession(host='192.168.1.21', user='jimmy', pswd='Spirent')
    vs = VelSession(host='10.190.15.229', user='jxie', pswd='Spirent-101')
    obj_inv = Inventory(vs)

    categories = obj_inv.get_categories()
    print(categories)
     
    devices = obj_inv.get_devices()
    print(devices)

    ports = obj_inv.get_ports()
    print(ports)
    print(len(ports))
     
    
    