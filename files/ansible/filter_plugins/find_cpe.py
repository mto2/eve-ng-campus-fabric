class FilterModule(object):

    def filters(self):
        return {
            'find_cpe': self.cleanup_site_prefixes,
        }

    def cleanup_site_prefixes(self, value, expectedvalue):
        # cpe = {}
        for each in value:
            if each['device_type'] == 'cpe':
                if expectedvalue == 'family':
                    return each['device_family_info']['family']
                elif expectedvalue == 'serial':
                    return each['device_serial_number']
