#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""newrelic_infra_condition_info module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: newrelic_infra_condition_info
short_description: Retrieve infra condition information
description:
    - Retrieve details about infra conditions.
    - Read-only module.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    host:
        description: API host address.
        type: str
        required: true
    condition_id:
        description: ID of a specific resource.
        type: str
    name:
        description: Filter by name.
        type: str
    username:
        description: Authentication username.
        type: str
    password:
        description: Authentication password.
        type: str
    api_key:
        description: API key for authentication.
        type: str
    validate_certs:
        description: Validate SSL certificates.
        type: bool
        default: true
    limit:
        description:
          - Maximum number of results to return.
        type: int
        default: 100
    offset:
        description:
          - Number of results to skip for pagination.
        type: int
        default: 0
"""

EXAMPLES = r"""
- name: List all
  stevefulme1.newrelic.newrelic_infra_condition_info:
    host: api.example.com
  register: result

- name: Get specific
  stevefulme1.newrelic.newrelic_infra_condition_info:
    host: api.example.com
    condition_id: "example-id"
  register: result
"""

RETURN = r"""
infra_conditions:
    description: List of resource details.
    returned: always
    type: list
    elements: dict
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
            limit=dict(type='int', default=100),
            offset=dict(type='int', default=0),
            condition_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    resource_id = module.params.get("condition_id")

    if resource_id:
        result = client.get("infra_condition", resource_id)
        resources = [result] if result else []
    else:
        resources = client.list("infra_condition", module.params)

    module.exit_json(changed=False, infra_conditions=resources)


if __name__ == "__main__":
    main()
