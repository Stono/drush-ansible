#!/usr/bin/python

DOCUMENTATION = '''
---
module: drush_cc
version_added: 1.0
author: "Karl Stoney (Stono)"
short_description: Manages drush cc 
description:
   - Allows you to manage drush cc 
options:
   name:
     description:
       - name of the cache to clear 
     required: true
requirements: ["drush"]
'''

EXAMPLES = '''
# clears all the cache 
- drush_cc: name=all
'''

import re

def _set(module):
    name = module.params['name']
    root = module.params['root']
    drush = module.params['drush']

    cmd = "{} cc {} --root={}".format(drush, name, root)
    result, stdout, stderr = module.run_command(cmd)

    if re.match(r'.*cache was cleared', stderr, re.S|re.M):
        module.exit_json(changed = True, result = "Cleared")
    elif result != 0:
        module.fail_json(msg="Failed to clear cache %s: %s" % (name, stderr))
    else:
        module.exit_json(changed = False, result = "Success")

def main():

    module = AnsibleModule(
        argument_spec = dict(
            name  = dict(required=True),
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
