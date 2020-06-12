class FilterModule(object):

    def filters(self):
        return {
            'snow_cleanup_site_name': self.snow_cleanup_site_name,
        }

    def snow_cleanup_site_name(self, value):
        value = value.replace(" ", "-")
        value = value.lower()
        return value