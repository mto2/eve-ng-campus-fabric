class FilterModule(object):

    def filters(self):
        return {
            'cleanup_device_prefixes': self.cleanup_device_prefixes,
        }

    def cleanup_device_prefixes(self, value):
        prefixes = {}
        data = {}
        voice = {}
        iot = {}
        pci = {}
        for each in value:
            if each["vrf"]["name"] == 'data':
                data["address"] = each["address"]
                data["description"] = each["description"]
                data["device"] = each["interface"]["device"]["display_name"]
                data["interface"] = each["interface"]["name"]
                data["name"] = each["vrf"]["name"]
                data["rd"] = each["vrf"]["rd"]
                data["tags"] = each["tags"]
                data["tenant"] = each["tenant"]["slug"]
            elif each["vrf"]["name"] == 'voice':
                voice["address"] = each["address"]
                voice["description"] = each["description"]
                voice["device"] = each["interface"]["device"]["display_name"]
                voice["interface"] = each["interface"]["name"]
                voice["name"] = each["vrf"]["name"]
                voice["rd"] = each["vrf"]["rd"]
                voice["tags"] = each["tags"]
                voice["tenant"] = each["tenant"]["slug"]
            elif each["vrf"]["name"] == 'iot':
                iot["address"] = each["address"]
                iot["description"] = each["description"]
                iot["device"] = each["interface"]["device"]["display_name"]
                iot["interface"] = each["interface"]["name"]
                iot["name"] = each["vrf"]["name"]
                iot["rd"] = each["vrf"]["rd"]
                iot["tags"] = each["tags"]
                iot["tenant"] = each["tenant"]["slug"]
            elif each["vrf"]["name"] == 'pci':
                pci["address"] = each["address"]
                pci["description"] = each["description"]
                pci["device"] = each["interface"]["device"]["display_name"]
                pci["interface"] = each["interface"]["name"]
                pci["name"] = each["vrf"]["name"]
                pci["rd"] = each["vrf"]["rd"]
                pci["tags"] = each["tags"]
                pci["tenant"] = each["tenant"]["slug"]
            else:
                pass
        
        prefixes['data'] = data
        prefixes['voice'] = voice
        prefixes['iot'] = iot
        prefixes['pci'] = pci
        return prefixes
