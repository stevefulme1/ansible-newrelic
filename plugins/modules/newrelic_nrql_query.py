#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)

"""Ansible module: newrelic_nrql_query."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: newrelic_nrql_query
short_description: Execute NRQL queries and return results
description:
    - Execute NRQL queries and return results in Newrelic.
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
    query:
        description: Unique identifier of the nrql result.
        type: str
    name:
        description: Display name of the nrql result.
        type: str
"""

EXAMPLES = r"""
- name: Create a nrql result
  stevefulme1.newrelic.newrelic_nrql_query:
    name: my-nrql-result
    state: present

- name: Delete a nrql result
  stevefulme1.newrelic.newrelic_nrql_query:
    query: "example-id"
    state: absent
"""

RETURN = r"""
nrql_result:
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
            query=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("query",)),
        ],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("query")

    if state == "present":
        if resource_id:
            result = client.update("nrql_result", resource_id, module.params)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("nrql_result", module.params)
        module.exit_json(changed=True, nrql_result=result)
    else:
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("nrql_result", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
