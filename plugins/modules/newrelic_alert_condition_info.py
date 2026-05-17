#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: newrelic_alert_condition_info."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: newrelic_alert_condition_info
short_description: Retrieve alert condition information
description:
    - Retrieve details about alert conditions.
    - This is a read-only module.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    host:
        description: API host address.
        type: str
        required: true
    username:
        description: Authentication username.
        type: str
    password:
        description: Authentication password.
        type: str
        no_log: true
    api_key:
        description: API key for authentication.
        type: str
        no_log: true
    validate_certs:
        description: Whether to validate SSL certificates.
        type: bool
        default: true

    condition_id:
        description: The condition id.
        type: str
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
- name: List all alert conditions
  stevefulme1.newrelic.newrelic_alert_condition_info:
  register: result

- name: Get a specific alert condition
  stevefulme1.newrelic.newrelic_alert_condition_info:
    condition_id: "example-id"
  register: result
"""

RETURN = r"""
alert_conditions:
    description: List of alert condition details.
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
        result = client.get("alert_condition", resource_id)
        resources = [result] if result else []
    else:
        resources = client.list("alert_condition", module.params)

    module.exit_json(changed=False, alert_conditions=resources)


if __name__ == "__main__":
    main()
