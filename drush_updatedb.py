#!/usr/bin/python

DOCUMENTATION = '''
---
module: drush_updatedb
version_added: 1.0
author: "Karl Stoney (Stono)"
short_description: Manages drush updatedb 
description:
   - Allows you to manage drush updatedb 
options:
requirements: ["drush"]
'''

EXAMPLES = '''
# Runs the database updates 
- drush_updatedb: root=/var/www
'''

import re

def _update(module):
    root = module.params['root']
    drush = module.params['drush']

    cmd = "{} updatedb -y --root={}".format(drush, root)
    result, stdout, stderr = module.run_command(cmd)

    if re.match(r'.*No database updates required', stderr, re.S|re.M):
        module.exit_json(changed = False, result = "Success")
    elif re.match(r'.*Finished performing updates', stderr, re.S|re.M):
        module.exit_json(changed = True, result = "Updated")
    elif result != 0:
        module.fail_json(msg="Failed to update the db: %s" % (stderr))
    else:
        module.exit_json(changed = False, result = "Success")

def main():

    module = AnsibleModule(
        argument_spec = dict(
            drush = dict(default='/opt/composer/vendor/bin/drush'),
            root = dict(required=True)
        ),
    )

    if module.params['drush'] == '':
        module.params['drush'] == drush

    _update(module)

# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
