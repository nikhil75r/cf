#!/usr/bin/python

from cfconfigurator.cf import CF
import json
import logging
import pprint
import sys
import trace
from ansible.module_utils.rad_cf_library import (
    get_org_guid,
    get_space_guid,
    get_apps_info)


DOCUMENTATION = '''
---
module: rad_cf_apps

short_description: Ansible module to find the apps in a space in Cloud Foundry

version_added: "1.0"

description:
    - "This RAD IT developed ansible module will look up a Cloud Foundry"
    - "org/space and return a list of all the apps that it finds there"

options:
    url:
        description:
            - This is a string defining the CF URL endpoint
        required: true
    username:
        description:
            - This is a string defining the CF Username
        required: true
    password:
        description:
            - This is a string defining the CF Password
        required: true
    org:
        description:
            - This is a string defining the CF Org
        required: true
    space:
        description:
            - This is a string defining the CF Space
        required: true

extends_documentation_fragment:
    - azure

author:
    - Philips Respironics - RAD IT
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
        changed=False,
        status=True,
        apps=[]
        apps_info=[]

changed:
    description: This module never changes the state of the target.
    type: bool
    value: False
status:
    description: Whether the run was successful or not
    type: bool
apps:
    description: A list of strings that reports the app names that were found
    type: list
apps_info:
    description: A list of dictionaries with info about the apps
    type: list
'''


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        url=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        org=dict(type='str', required=True),
        space=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        status=True,
        apps=[],
        apps_info=[]
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # log in to CF
    cf = CF(module.params['url'])
    logging.debug("Logging in")
    cf.login(module.params['username'], module.params['password'])

    # find org/space information
    cf_org_guid = get_org_guid(cf, module.params['org'])
    cf_space_guid = get_space_guid(cf, cf_org_guid, module.params['space'])

    # request the list of apps in the org/space
    apps = get_apps_info(cf, cf_org_guid, cf_space_guid)
    logging.debug("apps = '\n" + json.dumps(apps, indent=4) + "'")

    result['apps_info'] = apps

    for app in apps:
        result['apps'].append(app['name'])

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    logging.basicConfig(filename='/tmp/rad_cf_apps.log',
                        level=logging.DEBUG,
                        filemode='w')
    run_module()


if __name__ == '__main__':
    main()
