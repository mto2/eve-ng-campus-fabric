class FilterModule(object):

    def filters(self):
        return {
            'yaml_to_dict': self.yaml_to_dict,
        }

    def yaml_to_dict(self, value):
        import yaml
        return yaml.load(value, Loader=yaml.FullLoader)