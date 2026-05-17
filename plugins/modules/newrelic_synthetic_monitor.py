#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: newrelic_synthetic_monitor."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: newrelic_synthetic_monitor
short_description: Manage New Relic synthetic monitors
description:
    - Manage New Relic synthetic monitors in Newrelic.
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
"""

EXAMPLES = r"""
- name: Create a synthetic monitor
  stevefulme1.newrelic.newrelic_synthetic_monitor:
    name: my-synthetic-monitor
    state: present

- name: Delete a synthetic monitor
  stevefulme1.newrelic.newrelic_synthetic_monitor:
    monitor_id: "example-id"
    state: absent
"""

RETURN = r"""
synthetic_monitor:
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
            monitor_id=dict(type="str"),
            name=dict(type="str"),
            host=dict(type="str", required=True),
            username=dict(type="str"),
            password=dict(type="str", no_log=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("monitor_id",)),
        ],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required Python libraries not found.")

    client = ApiClient(module)
    state = module.params["state"]
    resource_id = module.params.get("monitor_id")

    if state == "present":
        existing = None
        if resource_id:
            existing = client.get("synthetic_monitor", resource_id)
        elif module.params.get("name"):
            candidates = client.list("synthetic_monitor", {{"name": module.params["name"]}})
            if candidates:
                existing = candidates[0]

        if existing:
            if module.check_mode:
                module.exit_json(changed=False, synthetic_monitor=existing)
            result = client.update("synthetic_monitor", resource_id or existing.get("id", ""), module.params)
            module.exit_json(changed=True, synthetic_monitor=result)
        else:
            if module.check_mode:
                module.exit_json(changed=True)
            result = client.create("synthetic_monitor", module.params)
            module.exit_json(changed=True, synthetic_monitor=result)
    else:
        existing = None
        if resource_id:
            existing = client.get("synthetic_monitor", resource_id)
        if not existing:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        client.delete("synthetic_monitor", resource_id)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
