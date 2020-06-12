class FilterModule(object):

    def filters(self):
        return {
            'cleanup_site_prefixes': self.cleanup_site_prefixes,
        }

    def cleanup_site_prefixes(self, value):
        prefixes = {}
        data = {}
        voice = {}
        iot = {}
        pci = {}
        for each in value:
            if each["vlan"]["name"] == 'data':
                data["name"] = each["vlan"]["name"]
                data["id"] = each["vlan"]["id"]
                data["vid"] = each["vlan"]["vid"]
                data["display_name"] = each["vlan"]["display_name"]
                data["prefix"] = each["prefix"]
                dhcp_root = each["prefix"][:-4]
                data["dhcp_low"] = dhcp_root + "10"
                data["dhcp_high"] = dhcp_root + "250"
                data["description"] = each["description"]
                data["tags"] = each["tags"]
                data["site"] = each["site"]["slug"]
                data["tenant"] = each["tenant"]["slug"]
                try:
                    data["vrf"] = each["vrf"]["name"]
                except:
                    continue
            elif each["vlan"]["name"] == 'voice':
                voice["name"] = each["vlan"]["name"]
                voice["id"] = each["vlan"]["id"]
                voice["vid"] = each["vlan"]["vid"]
                voice["display_name"] = each["vlan"]["display_name"]
                voice["prefix"] = each["prefix"]
                dhcp_root = each["prefix"][:-4]
                voice["dhcp_low"] = dhcp_root + "10"
                voice["dhcp_high"] = dhcp_root + "250"
                voice["description"] = each["description"]
                voice["tags"] = each["tags"]
                voice["site"] = each["site"]["slug"]
                voice["tenant"] = each["tenant"]["slug"]
                try:
                    voice["vrf"] = each["vrf"]["name"]
                except:
                    continue
            elif each["vlan"]["name"] == 'iot':
                iot["name"] = each["vlan"]["name"]
                iot["id"] = each["vlan"]["id"]
                iot["vid"] = each["vlan"]["vid"]
                iot["display_name"] = each["vlan"]["display_name"]
                iot["prefix"] = each["prefix"]
                dhcp_root = each["prefix"][:-4]
                iot["dhcp_low"] = dhcp_root + "10"
                iot["dhcp_high"] = dhcp_root + "250"
                iot["description"] = each["description"]
                iot["tags"] = each["tags"]
                iot["site"] = each["site"]["slug"]
                iot["tenant"] = each["tenant"]["slug"]
                try:
                    iot["vrf"] = each["vrf"]["name"]
                except:
                    continue
            elif each["vlan"]["name"] == 'pci':
                pci["name"] = each["vlan"]["name"]
                pci["id"] = each["vlan"]["id"]
                pci["vid"] = each["vlan"]["vid"]
                pci["display_name"] = each["vlan"]["display_name"]
                pci["prefix"] = each["prefix"]
                dhcp_root = each["prefix"][:-4]
                pci["dhcp_low"] = dhcp_root + "10"
                pci["dhcp_high"] = dhcp_root + "250"
                pci["description"] = each["description"]
                pci["tags"] = each["tags"]
                pci["site"] = each["site"]["slug"]
                pci["tenant"] = each["tenant"]["slug"]
                try:
                    pci["vrf"] = each["vrf"]["name"]
                except:
                    continue
            else:
                pass
        
        prefixes['data'] = data
        prefixes['voice'] = voice
        prefixes['iot'] = iot
        prefixes['pci'] = pci
        return prefixes
