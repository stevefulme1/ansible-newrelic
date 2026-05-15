#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)

"""Ansible module: newrelic_service_level."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: newrelic_service_level
short_description: Manage New Relic SLI/SLO objectives
description:
    - Manage New Relic SLI/SLO objectives in Newrelic.
    - Supports create, update, and delete operations.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the resource.
        type: str
        default: present
        choices: [present, absent]
    sli_guid:
        description: Unique identifier of the service level.
        type: str
    name:
        description: Display name of the service level.
        type: str
"""

EXAMPLES = r"""
- name: Create a service level
  stevefulme1.newrelic.newrelic_service_level:
    name: my-service-level
    state: present

- name: Delete a service level
  stevefulme1.newrelic.newrelic_service_level:
    sli_guid: "example-id"
    state: absent
"""

RETURN = r"""
service_level:
    description: Resource details.
    returned: on success
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.stevefulme1.newrelic.plugins.module_utils.api_client import ApiClient
    HAS_CLIENT = True
except ImportError:
    HAS_CLIENT = False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            sli_guid=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("sli_guid",)),
        ],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("sli_guid")

    if state == "present":
        if resource_id:
            result = client.update("service_level", resource_id, module.params)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("service_level", module.params)
        module.exit_json(changed=True, service_level=result)
    else:
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("service_level", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
