#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import json
import re


def cleanup_vlans(vlans):
    """ 
    // cleaning up the vlans object to make it easier to work with later on
    // iterates over the list of vlans
    // try / except to help build k/v where none exists natively (ie. description)
    """
    vlan_list = []
    for each in vlans['vlan']:
        info = {}
        vlan_id = each['vlan-id']
        try:
            vni_id = each['vxlan']['vni']
        except:
            vni_id = None
        try:
            description = each['description']
        except:
            description = None
        try:
            l3_interface = each['l3-interface']
        except:
            l3_interface = None
        info['vlan_id'] = vlan_id
        info['vni_id'] = vni_id
        info['description'] = description
        info['l3_interface'] = l3_interface
        vlan_list.append(info)
    return(vlan_list)


def cleanup_irbs(irbs):
    """ 
    // extracting the irb interface from a list of all interfaces
    """
    iface_irb = []
    for each in irbs['interface']:
        # info = {}
        if each['name'] == 'irb':
            iface_irb.append(each)

    """ 
    // cleaning up the irb information to make the object easier to work with later on
    // iterates over the list of irb interfaces
    // logic loops over ipv4 address if it is stored in a list, simple mapping if it's a dict
    """
    inet_addresses = []
    for each in iface_irb[0]['unit']:
        info = {}
        name = each['name']
        try:
            if isinstance(each['family']['inet']['address'], list):
                inet_address = []
                for inet in each['family']['inet']['address']:
                    inet_address.append(inet)
            else:
                inet_address = [each['family']['inet']['address']]
        except:
            inet_address = None
        info['name'] = name
        info['inet_address'] = inet_address
        inet_addresses.append(info)
    return(inet_addresses)


def was_vni_imported(vlans, vrf_import):
    vni_imported = []
    
    for each in vlans:
        for import_as in vrf_import['import-as']:
            if isinstance(import_as['vni-list'], list):
                for item in import_as['vni-list']:
                    if str(each['vni_id']) == str(item):
                        info = {}
                        info['vlan_id'] = each['vlan_id']
                        info['vni_id'] = each['vni_id']
                        info['description'] = each['description']
                        info['l3_interface'] = each['l3_interface']
                        info['import_as'] = import_as['name']
                        vni_imported.append(info)
            else:
                if str(each['vni_id']) == str(import_as['vni-list']):
                    info = {}
                    info['vlan_id'] = each['vlan_id']
                    info['vni_id'] = each['vni_id']
                    info['description'] = each['description']
                    info['l3_interface'] = each['l3_interface']
                    info['import_as'] = import_as['name']
                    vni_imported.append(info)
    
    return(vni_imported)


def bind_vlan_irb(vlans, irbs):
    """ 
    // binding the vlan/vxlan/ip information into a single object
    // iterates over the list of vlans since our VNI is the unique object
    // finds where the vlan and irb unit match, then builds single dict object based on values in both
    """
    interfaces = []
    for each in vlans:
        for irb in irbs:
            if each['vlan_id'] == irb['name']:
                info = {}
                info['irb_unit'] = irb['name']
                info['ipv4'] = irb['inet_address']
                info['vlan_id'] = each['vlan_id']
                info['vni_id'] = each['vni_id']
                info['description'] = each['description']
                info['l3_interface'] = each['l3_interface']
                info['import_as'] = each['import_as']
                interfaces.append(info)
    return(interfaces)


def main():
    """ 
    // create a object 'module' with the AnsibleModule function we imported at the top of the file
    // defined mandatory fields to be passed from the Ansible playbook
    // specify which fields are strings and which are dictionaries
    """
    module = AnsibleModule(
        argument_spec = dict(
            inventory_hostname = dict(required=True, type='str'),
            vlans = dict(required=True, type='dict'),
            vrf_import = dict(required=True, type='dict'),
            irbs = dict(required=True, type='dict')
        )
    )

    """ 
    // main entry point for module execution
    // creates new python objects based on the data passed from playbook
    """
    inventory_hostname = (module.params['inventory_hostname'])
    vlans = (module.params['vlans'])
    vrf_import = (module.params['vrf_import'])
    irbs = (module.params['irbs'])

    """ 
    // cleanup section, passing our new objects through to cleanup functions
    """
    vlans = cleanup_vlans(vlans)
    vlans = was_vni_imported(vlans, vrf_import)
    irbs = cleanup_irbs(irbs)
    interfaces = bind_vlan_irb(vlans, irbs)

    """ 
    // create an object storing our cleaned up information
    // sends object back to playbook
    """
    response = {'inventory_hostname': inventory_hostname, 'interfaces': interfaces}
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
