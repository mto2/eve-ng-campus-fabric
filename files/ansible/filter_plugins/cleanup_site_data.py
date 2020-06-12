class FilterModule(object):

    def filters(self):
        return {
            'cleanup_site_data': self.cleanup_site_data,
        }

    def cleanup_site_data(self, value):
        site = {}
        for each in value:
            site["name"] = each["name"]
            site["slug"] = each["slug"]
            site["region"] = each["region"]["slug"]
            site["country"] = each["region"]["name"]
            site["tenant"] = each["tenant"]["slug"]
            site["facility"] = each["facility"]
            site["asn"] = each["asn"]
            site["time_zone"] = each["time_zone"]
            site["description"] = each["description"]
            site["physical_address"] = each["physical_address"]
            address = each["physical_address"].split(',')
            site["street_address"] = address[0]
            site["city"] = str(address[1]).strip()
            site["state"] = str(address[2]).strip()
            site["latitude"] = each["latitude"]
            site["longitude"] = each["longitude"]
            site["contact_name"] = each["contact_name"]
            site["contact_phone"] = each["contact_phone"]
            site["contact_email"] = each["contact_email"]
        
        return site