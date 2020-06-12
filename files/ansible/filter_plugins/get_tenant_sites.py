class FilterModule(object):

    def filters(self):
        return {
            'get_tenant_sites': self.get_tenant_sites,
        }

    def get_tenant_sites(self, value):
        import json
        sites = []

        for each in value['tenant-sites']:
          site = {}
          for fq in each['fq_name']:
            if "OAM" in fq:
              pass
            elif "JNPR" in fq:
              pass
            else:
              site["name"] = each["fq_name"][0]
              site["uuid"] = each["uuid"]
              site["href"] = each["href"]
              sites.append(site)
        return sites
