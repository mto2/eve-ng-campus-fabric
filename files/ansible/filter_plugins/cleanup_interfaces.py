class FilterModule(object):

    def filters(self):
        return {
            'cleanup_interfaces': self.cleanup_interfaces,
        }

    def cleanup_interfaces(self, value):
        import requests
        import json
        # ##########################################################
        # ### Netbox information (to be used for IPAM lookups later)
        # ########################################################## 
        api_token = "ad34740e10bde714f96960addf42b36db6c28c0e"
        baseurl = "https://netbox.server.home/api/ipam/ip-addresses/"

        # ##########################################################
        # ### all devices
        # ########################################################## 
        devices = []
        
        # ###
        # ### iterate over the list of devices
        # ###
        for each_device in value:
            # ##########################################################
            # ### each device
            # ########################################################## 
            device = {}

            # device name
            device["hostname"] = each_device["item"]["name"]

            # device platform
            try:
                device["platform"] = each_device["item"]["platform"]
            except KeyError:
                device["platform"] = "juniper_junos"

            # device serial number
            try:
                device["serial"] = each_device["item"]["serial"]
            except KeyError:
                device["serial"] = "abcdefghi"

            # site name
            try:
                device["site"] = each_device["item"]["site"]
            except KeyError:
                device["site"] = "pancakes"

            # tenant name
            try:
                device["tenant"] = each_device["item"]["tenant"]
            except KeyError:
                device["tenant"] = "syrup"

            # ##########################################################
            # ### each interface
            # ########################################################## 

            # first create an empty list to hold all interfaces after append
            device["interfaces"] = []

            for each in each_device["json"]["results"]:
                interface = {}

                # interface name
                try:
                    interface["name"] = each["name"]
                except KeyError:
                    interface["name"] = "nonameinterface"

                # interface description
                try:
                    interface["description"] = each["description"]
                except KeyError:
                    interface["description"] = ""

                # routed interface
                try:
                    interface["count_ipaddresses"] = each["count_ipaddresses"]
                except KeyError:
                    pass

                # trunk or access interface
                try:
                    if each["mode"] is not None:
                        if each["mode"]["value"] == "tagged":
                            interface["mode"] = "trunk"
                        elif each["mode"]["value"] == "access":
                            interface["mode"] = "access"
                    else:
                        pass
                except AttributeError:
                    pass

                # interface enabled or disabled
                try:
                    interface["enabled"] = each["enabled"]
                except KeyError:
                    pass

                # interface mtu
                try:
                    interface["mtu"] = each["mtu"]
                except KeyError:
                    pass

                # tagged vlans
                try:
                    if len(each["tagged_vlans"]) > 0:
                        tagged_vlans = []
                        for each_vlan in each["tagged_vlans"]:
                            vlan = {}
                            vlan["name"] = each_vlan["name"]
                            vlan["vid"] = each_vlan["vid"]
                            tagged_vlans.append(vlan)
                        interface["tagged_vlans"] = tagged_vlans
                    else:
                        pass
                except AttributeError:
                    pass

                # untagged vlans
                try:
                    if each["untagged_vlan"] is not None:
                        untagged_vlan = {}
                        # untagged_vlan["display_name"] = each["untagged_vlan"]["display_name"]
                        # untagged_vlan["id"] = each["untagged_vlan"]["id"]
                        untagged_vlan["name"] = each["untagged_vlan"]["name"]
                        # untagged_vlan["url"] = each["untagged_vlan"]["url"]
                        untagged_vlan["vid"] = each["untagged_vlan"]["vid"]
                        interface["untagged_vlan"] = untagged_vlan
                    else:
                        pass
                except KeyError:
                    pass

                # lag interface
                try:
                    if each["lag"] is not None:
                        interface["lag"] = each["lag"]["name"]
                    else:
                        pass
                except KeyError:
                    pass

                # ip address
                try:
                    if interface["count_ipaddresses"] > 0:
                        ipv4 = {}
                        ipv6 = {}
                        ipv4_addresses = []
                        ipv6_addresses = []
                        device_id = each["device"]["id"]
                        iface = each["name"]

                        # let's make a rest api query to netbox's ipam for more info
                        # pulls baseurl and api_token from very top of this script
                        try:
                            response = requests.get(
                                url=baseurl,
                                params={
                                    "device_id": device_id,
                                    "interface": iface,
                                },
                                headers={
                                    "Authorization": "Token " + api_token,
                                    "Content-Type": "application/json; charset=utf-8",
                                },
                                verify=False
                            )
                            content = json.loads(response.content)

                            # assign IPv4 and IPv6 addresses
                            for each in content["results"]:

                                # ipv4
                                if each["family"]["label"] == "IPv4":
                                    ipv4 = {}
                                    
                                    # append ipv4 address to list
                                    address = each["address"]

                                    # tags
                                    tags = each["tags"]
                                    
                                    # find the role of the IPv4 address
                                    if each["role"] is not None:
                                        if each["role"]["value"] == "anycast":
                                            role = "virtual_gateway_anycast"
                                            address = address.split('/')
                                            address = address[0]
                                        elif each["role"]["value"] == "secondary":
                                            role = "physical_address"
                                    else:
                                        role = 'undefined'
                                    
                                    ipv4["address"] = address
                                    ipv4["tags"] = tags
                                    ipv4["role"] = role
                                    ipv4_addresses.append(ipv4)

                                # ipv6
                                else:
                                    ipv6 = {}

                                    # append ipv6 address to list
                                    address = each["address"]

                                    # assign tags
                                    tags = each["tags"]

                                    # find the role of the IPv6 address
                                    if each["role"] is not None:
                                        if each["role"]["value"] == "anycast":
                                            role = "virtual_gateway_anycast"
                                            address = address.split('/')
                                            address = address[0]
                                        elif each["role"]["value"] == "secondary":
                                            role = "physical_address"
                                    else:
                                        role = 'undefined'
                                    
                                    ipv6["address"] = address
                                    ipv6["tags"] = tags
                                    ipv6["role"] = role
                                    ipv6_addresses.append(ipv6)

                            if len(ipv4_addresses) > 0:
                                interface["ipv4"] = ipv4_addresses
                            if len(ipv6_addresses) > 0:
                                interface["ipv6"] = ipv6_addresses
                        except requests.exceptions.RequestException:
                            interface["ipv4"] = "failed"

                    else:
                        pass
                except KeyError:
                    pass

                # append the interface to the list of interfaces
                device["interfaces"].append(interface)
            
            # ##########################################################
            # ### append each device (and its interfaces) to devices
            # ########################################################## 
            devices.append(device)

        return devices