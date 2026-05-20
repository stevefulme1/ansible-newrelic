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
    - Create, update, and delete New Relic synthetic monitors using the Synthetics API v3.
    - "API reference: GET/POST/PUT/DELETE /v3/monitors/{id}"
    - Supports full idempotency and check_mode with diff.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the synthetic monitor.
        type: str
        default: present
        choices: [present, absent]
    monitor_id:
        description:
            - The ID of the synthetic monitor.
            - Required when O(state=absent).
        type: str
    name:
        description: Name of the monitor.
        type: str
    monitor_type:
        description: Type of monitor (SIMPLE, BROWSER, SCRIPT_API, SCRIPT_BROWSER).
        type: str
        choices: [SIMPLE, BROWSER, SCRIPT_API, SCRIPT_BROWSER]
    uri:
        description: URI to monitor (for SIMPLE and BROWSER types).
        type: str
    frequency:
        description: Check frequency in minutes.
        type: int
    locations:
        description: Locations to run the monitor from.
        type: list
        elements: str
    status:
        description: Monitor status (ENABLED or DISABLED).
        type: str
        choices: [ENABLED, DISABLED]
    sla_threshold:
        description: SLA threshold in seconds.
        type: float
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
- name: Create a simple ping monitor
  stevefulme1.newrelic.newrelic_synthetic_monitor:
    host: api.newrelic.com
    api_key: "{{ newrelic_api_key }}"
    state: present
    name: Homepage Ping
    monitor_type: SIMPLE
    uri: "https://example.com"
    frequency: 5
    locations:
      - AWS_US_EAST_1
      - AWS_EU_WEST_1
    status: ENABLED

- name: Delete a synthetic monitor by ID
  stevefulme1.newrelic.newrelic_synthetic_monitor:
    host: api.newrelic.com
    api_key: "{{ newrelic_api_key }}"
    monitor_id: "abc-123-def"
    state: absent
"""

RETURN = r"""
synthetic_monitor:
    description: The synthetic monitor resource returned by the New Relic API.
    returned: on success
    type: dict
    sample:
        id: abc-123-def
        name: Homepage Ping
        type: SIMPLE
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
    """Fetch current synthetic monitor state. Returns None if not found (404)."""
    resource_id = module.params.get("monitor_id")
    if resource_id:
        return client.get("synthetic_monitor", resource_id)
    name = module.params.get("name")
    if name:
        return client.find_by_name("synthetic_monitor", name)
    return None


def build_payload(module):
    """Build the API payload from module params."""
    payload = {}
    field_map = {
        "name": "name",
        "monitor_type": "type",
        "uri": "uri",
        "frequency": "frequency",
        "locations": "locations",
        "status": "status",
        "sla_threshold": "slaThreshold",
    }
    for param, api_field in field_map.items():
        value = module.params.get(param)
        if value is not None:
            payload[api_field] = value
    return payload


def needs_update(current, desired):
    """Compare current API state against desired params. Returns True if different."""
    for key, desired_val in desired.items():
        if desired_val is None:
            continue
        current_val = current.get(key)
        if isinstance(desired_val, list) and isinstance(current_val, list):
            if sorted(desired_val) != sorted(current_val):
                return True
        elif current_val != desired_val:
            return True
    return False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            monitor_id=dict(type="str"),
            name=dict(type="str"),
            monitor_type=dict(
                type="str",
                choices=["SIMPLE", "BROWSER", "SCRIPT_API", "SCRIPT_BROWSER"],
            ),
            uri=dict(type="str"),
            frequency=dict(type="int"),
            locations=dict(type="list", elements="str"),
            status=dict(type="str", choices=["ENABLED", "DISABLED"]),
            sla_threshold=dict(type="float"),
            host=dict(type="str", required=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("monitor_id",)),
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
                resource_id = current.get("id", module.params.get("monitor_id", ""))
                diff = {"before": current, "after": payload}
                if module.check_mode:
                    module.exit_json(changed=True, synthetic_monitor=current, diff=diff)
                result = client.update("synthetic_monitor", resource_id, payload)
                module.exit_json(changed=True, synthetic_monitor=result, diff=diff)
            else:
                module.exit_json(changed=False, synthetic_monitor=current)
        else:
            if module.check_mode:
                module.exit_json(changed=True, diff={"before": {}, "after": payload})
            result = client.create("synthetic_monitor", payload)
            module.exit_json(changed=True, synthetic_monitor=result,
                             diff={"before": {}, "after": payload})
    else:
        if not current:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True, diff={"before": current, "after": {}})
        client.delete("synthetic_monitor", module.params["monitor_id"])
        module.exit_json(changed=True, diff={"before": current, "after": {}})


if __name__ == "__main__":
    main()
