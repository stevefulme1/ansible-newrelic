#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: newrelic_dashboard."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: newrelic_dashboard
short_description: Manage New Relic dashboards via NerdGraph
description:
    - Create, update, and delete New Relic dashboards using the NerdGraph API.
    - "API reference: mutation { dashboardCreate / dashboardUpdate / dashboardDelete }"
    - Supports full idempotency and check_mode with diff.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the dashboard.
        type: str
        default: present
        choices: [present, absent]
    dashboard_guid:
        description:
            - The GUID of the dashboard entity.
            - Required when O(state=absent).
        type: str
    name:
        description: Name of the dashboard.
        type: str
    description:
        description: Description of the dashboard.
        type: str
    permissions:
        description: Dashboard permissions (PUBLIC_READ_WRITE, PUBLIC_READ_ONLY, PRIVATE).
        type: str
        choices: [PUBLIC_READ_WRITE, PUBLIC_READ_ONLY, PRIVATE]
    pages:
        description: List of dashboard page definitions.
        type: list
        elements: dict
    account_id:
        description: New Relic account ID.
        type: int
    host:
        description: New Relic API host (e.g. api.newrelic.com).
        type: str
        required: true
    api_key:
        description: New Relic API key.
        type: str
        no_log: true
    validate_certs:
        description: Whether to validate SSL certificates.
        type: bool
        default: true
"""

EXAMPLES = r"""
- name: Create a dashboard via NerdGraph
  stevefulme1.newrelic.newrelic_dashboard:
    host: api.newrelic.com
    api_key: "{{ newrelic_api_key }}"
    state: present
    name: Application Overview
    account_id: 12345
    permissions: PUBLIC_READ_WRITE
    pages:
      - name: Overview
        widgets:
          - title: Throughput
            configuration:
              area:
                nrqlQueries:
                  - query: "SELECT rate(count(*), 1 minute) FROM Transaction"

- name: Delete a dashboard by GUID
  stevefulme1.newrelic.newrelic_dashboard:
    host: api.newrelic.com
    api_key: "{{ newrelic_api_key }}"
    dashboard_guid: "MTIzNDU2fFZJWnxEQVNIQk9BUkR8MTIzNDU2"
    state: absent
"""

RETURN = r"""
dashboard:
    description: The dashboard entity returned by NerdGraph.
    returned: on success
    type: dict
    sample:
        guid: MTIzNDU2fFZJWnxEQVNIQk9BUkR8MTIzNDU2
        name: Application Overview
diff:
    description: Before/after state for check_mode and changes.
    returned: when changed
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.stevefulme1.newrelic.plugins.module_utils.api_client import ApiClient
    HAS_CLIENT = True
except ImportError:
    HAS_CLIENT = False


def get_current_state(client, module):
    """Fetch current dashboard state. Returns None if not found."""
    guid = module.params.get("dashboard_guid")
    if guid:
        return client.get("dashboard", guid)
    name = module.params.get("name")
    if name:
        return client.find_by_name("dashboard", name)
    return None


def build_payload(module):
    """Build the NerdGraph dashboard input from module params."""
    payload = {}
    for param in ("name", "description", "permissions", "pages"):
        value = module.params.get(param)
        if value is not None:
            payload[param] = value
    account_id = module.params.get("account_id")
    if account_id is not None:
        payload["account_id"] = account_id
    return payload


def needs_update(current, desired):
    """Compare current NerdGraph entity against desired params. Returns True if different."""
    for key, desired_val in desired.items():
        if desired_val is None or key == "account_id":
            continue
        current_val = current.get(key)
        if isinstance(desired_val, list) and isinstance(current_val, list):
            if desired_val != current_val:
                return True
        elif current_val != desired_val:
            return True
    return False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            dashboard_guid=dict(type="str"),
            name=dict(type="str"),
            description=dict(type="str"),
            permissions=dict(
                type="str",
                choices=["PUBLIC_READ_WRITE", "PUBLIC_READ_ONLY", "PRIVATE"],
            ),
            pages=dict(type="list", elements="dict"),
            account_id=dict(type="int"),
            host=dict(type="str", required=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("dashboard_guid",)),
            ("state", "present", ("name",)),
        ],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required library 'requests' is not installed.")

    client = ApiClient(module)
    state = module.params["state"]

    current = get_current_state(client, module)
    payload = build_payload(module)

    if state == "present":
        if current:
            if needs_update(current, payload):
                guid = current.get("guid", module.params.get("dashboard_guid", ""))
                diff = {"before": current, "after": payload}
                if module.check_mode:
                    module.exit_json(changed=True, dashboard=current, diff=diff)
                result = client.update("dashboard", guid, payload)
                module.exit_json(changed=True, dashboard=result, diff=diff)
            else:
                module.exit_json(changed=False, dashboard=current)
        else:
            if module.check_mode:
                module.exit_json(changed=True, diff={"before": {}, "after": payload})
            result = client.create("dashboard", payload)
            module.exit_json(changed=True, dashboard=result,
                             diff={"before": {}, "after": payload})
    else:
        if not current:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True, diff={"before": current, "after": {}})
        client.delete("dashboard", module.params["dashboard_guid"])
        module.exit_json(changed=True, diff={"before": current, "after": {}})


if __name__ == "__main__":
    main()
