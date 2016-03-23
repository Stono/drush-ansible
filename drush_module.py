#!/usr/bin/python

DOCUMENTATION = '''
---
module: drush_module
version_added: 1.0
author: "Karl Stoney (Stono)"
short_description: Manages drush modules 
description:
   - Allows you to manage drush modules 
options:
   name:
     description:
       - name of the module 
     required: true
   state:
     description:
       - indicate the desired state of the module
     choices: ['enabled', 'disabled', 'absent']
     required: true
requirements: ["drush"]
'''

EXAMPLES = '''
# enables the drush module "dancing_queen"
- drush_module: state=enabled name=dancing_queen
'''

import re

def _disable_module(module):
    name = module.params['name']
    root = module.params['root']
    drush = module.params['drush']

    cmd = "{} dis -y {} --root={}".format(drush, name, root)
    result, stdout, stderr = module.run_command(cmd)

    if re.match(r'.*was disabled successfully', stderr, re.S|re.M):
        module.exit_json(changed = True, result = "Disabled")
    elif result != 0:
        module.fail_json(msg="Failed to disable module %s: %s" % (name, stderr))
    else:
        module.exit_json(changed = False, result = "Success")

def _absent_module(module):
    name = module.params['name']
    root = module.params['root']
    drush = module.params['drush']

    cmd = "{} pm-uninstall -y {} --root={}".format(drush, name, root)
    result, stdout, stderr = module.run_command(cmd)

    if re.match(r'.*was successfully uninstalled', stderr, re.S|re.M):
        module.exit_json(changed = True, result = "Success")
    elif result != 0:
        module.fail_json(msg="Failed to remove module %s: %s" % (name, stderr))
    else:
        module.exit_json(changed = False, result = "Removed")

def _enable_module(module):
    name = module.params['name']
    root = module.params['root']
    drush = module.params['drush']

    cmd = "{} en -y {} --root={}".format(drush, name, root)
    result, stdout, stderr = module.run_command(cmd)

    if re.match(r'.*was enabled successfully', stderr, re.S|re.M):
        module.exit_json(changed = True, result = "Success")
    elif re.match(r'.*was not found', stderr, re.S|re.M):
        module.fail_json(msg="Module %s was not found so it could not be enabled!" % (name))
    elif result != 0:
        module.fail_json(msg="Failed to enable module %s: %s" % (name, stderr))
    else:
        module.exit_json(changed = False, result = "Enabled")

def main():

    module = AnsibleModule(
        argument_spec = dict(
            name  = dict(required=True),
            state = dict(required=True, choices=['enabled', 'disabled', 'absent']),
            drush = dict(default='/opt/composer/vendor/bin/drush'),
            root = dict(required=True)
        ),
    )

    if module.params['state'] == 'absent':
        _absent_module(module)

    if module.params['state'] == 'disabled':
        _disable_module(module)

    if module.params['state'] == 'enabled':
        _enable_module(module)

# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
