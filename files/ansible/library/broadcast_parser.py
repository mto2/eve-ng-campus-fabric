#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import json
import re


def cleanup_interfaces(interfaces):
    """ 
    // extracting the irb interface from a list of all interfaces
    """
    iface = []
    for each in interfaces:
        # info = {}
        if each['admin-status'] == 'up':
            iface.append(each)

    """ 
    // cleaning up the irb information to make the object easier to work with later on
    // iterates over the list of irb interfaces
    // logic loops over ipv4 address if it is stored in a list, simple mapping if it's a dict
    """
    iface_ethernet_stats = []
    for each in iface:
        info = {}
        if "ethernet-mac-statistics" in each.keys():
            info['stats'] = each["ethernet-mac-statistics"]
            iface_ethernet_stats.append(info)
    return(iface_ethernet_stats)


def main():
    """ 
    // create a object 'module' with the AnsibleModule function we imported at the top of the file
    // defined mandatory fields to be passed from the Ansible playbook
    // specify which fields are strings and which are dictionaries
    """
    module = AnsibleModule(
        argument_spec = dict(
            inventory_hostname = dict(required=True, type='str'),
            interfaces = dict(required=True, type='list')
        )
    )

    """ 
    // main entry point for module execution
    // creates new python objects based on the data passed from playbook
    """
    inventory_hostname = (module.params['inventory_hostname'])
    interfaces = (module.params['interfaces'])

    """ 
    // cleanup section, passing our new objects through to cleanup functions
    """
    interfaces = cleanup_interfaces(interfaces)

    """ 
    // create an object storing our cleaned up information
    // sends object back to playbook
    """
    response = {'inventory_hostname': inventory_hostname, 'interfaces': interfaces}
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
