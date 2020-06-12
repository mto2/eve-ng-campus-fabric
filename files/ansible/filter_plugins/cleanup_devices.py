class FilterModule(object):

    def filters(self):
        return {
            'cleanup_devices': self.cleanup_devices,
        }

    def cleanup_devices(self, value):
        site_devices = []
        for each in value:
            device = {}
            device['name'] = each['name']
            device['tenant'] = each['tenant']['slug']
            device['platform'] = each['platform']['name']
            device['serial'] = each['serial']
            device['site'] = each['site']['slug']
            site_devices.append(device)
        
        return site_devices