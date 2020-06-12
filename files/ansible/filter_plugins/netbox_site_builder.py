class FilterModule(object):

    def filters(self):
        return {
            'netbox_site_builder': self.netbox_site_builder,
        }

    def netbox_site_builder(self, value):
        import random
        name_first = value['name']
        name_last = value['maiden_name']
        name_last = name_last.lower()
        site_name = 'site-' + name_last[-4:]
        latitude = value['latitude']
        latitude = str(latitude)
        latitude = latitude[:8]
        longitude = value['longitude']
        longitude = str(longitude)
        longitude = longitude[:8]
        address = value['address']
        email_u = value['email_u']
        email_d = value['email_d']
        company = value['company']
        phone = value['phone_w']
        domain = value['domain']
        url = value['url']

        site = {
            "name": site_name,
            "slug": name_last,
            "status": "active",
            "region": 1,
            "tenant": 1,
            "facility": company,
            "asn": random.randint(1, 65535),
            "time_zone": "America/Phoenix",
            "description": domain,
            "physical_address": address,
            "latitude": latitude,
            "longitude": longitude,
            "contact_name": name_first,
            "contact_phone": phone,
            "contact_email": email_u + "@" + email_d,
            "comments": company,
            "tags": [
                "retail",
                "spoke",
                "sdwan"
            ],
        }

        return site