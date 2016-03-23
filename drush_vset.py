#!/usr/bin/python

DOCUMENTATION = '''
---
module: drush_vset
version_added: 1.0
author: "Karl Stoney (Stono)"
short_description: Manages drush settings 
description:
   - Allows you to manage drush settings 
options:
   name:
     description:
       - name of the setting 
     required: true
   state:
     value:
       - indicate the desired value of the value
     required: true
requirements: ["drush"]
'''

EXAMPLES = '''
# sets the dancing_queen variable to is_bad
- drush_vset: value=is_bad name=dancing_queen
'''

import re

def _set(module):
    name = module.params['name']
    value = module.params['value']
    root = module.params['root']
    drush = module.params['drush']

    # First get it
    cmd = "{} vget {} --exact --format=string --root={}".format(drush, name, root)
    result, stdout, stderr = module.run_command(cmd)

    if re.match(r'.*' + value, stdout, re.S|re.M):
        return module.exit_json(changed = False, result = "Already Set")

    cmd = "{} vset {} {} --root={}".format(drush, name, value, root)
    result, stdout, stderr = module.run_command(cmd)

    if re.match(r'.*was set to', stderr, re.S|re.M):
        module.exit_json(changed = True, result = "Set")
    elif result != 0:
        module.fail_json(msg="Failed to set variable %s: %s" % (name, stderr))
    else:
        module.exit_json(changed = False, result = "Success")

def main():

    module = AnsibleModule(
        argument_spec = dict(
            name  = dict(required=True),
            value  = dict(required=True),
            drush = dict(default='/opt/composer/vendor/bin/drush'),
            root = dict(required=True)
        ),
    )

    if module.params['drush'] == '':
        module.params['drush'] == drush

    _set(module)

# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
