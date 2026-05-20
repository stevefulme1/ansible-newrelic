#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module: newrelic_alert_policy."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: newrelic_alert_policy
short_description: Manage New Relic alert policies
description:
    - Create, update, and delete New Relic alert policies via the REST API v2.
    - "API reference: GET/POST/PUT/DELETE /v2/alerts_policies/{id}.json"
    - Supports full idempotency and check_mode with diff.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    state:
        description: Desired state of the alert policy.
        type: str
        default: present
        choices: [present, absent]
    policy_id:
        description:
            - The ID of the alert policy.
            - Required when O(state=absent).
        type: str
    name:
        description: Name of the alert policy.
        type: str
    incident_preference:
        description: Incident preference (PER_POLICY, PER_CONDITION, PER_CONDITION_AND_TARGET).
        type: str
        choices: [PER_POLICY, PER_CONDITION, PER_CONDITION_AND_TARGET]
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
- name: Create an alert policy
  stevefulme1.newrelic.newrelic_alert_policy:
    host: api.newrelic.com
    api_key: "{{ newrelic_api_key }}"
    state: present
    name: Production Alerts
    incident_preference: PER_POLICY

- name: Delete an alert policy by ID
  stevefulme1.newrelic.newrelic_alert_policy:
    host: api.newrelic.com
    api_key: "{{ newrelic_api_key }}"
    policy_id: "12345"
    state: absent
"""

RETURN = r"""
alert_policy:
    description: The alert policy resource returned by the New Relic API.
    returned: on success
    type: dict
    sample:
        id: 12345
        name: Production Alerts
        incident_preference: PER_POLICY
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
    """Fetch current alert policy state. Returns None if not found (404)."""
    resource_id = module.params.get("policy_id")
    if resource_id:
        return client.get("alert_policy", resource_id)
    name = module.params.get("name")
    if name:
        return client.find_by_name("alert_policy", name)
    return None


def build_payload(module):
    """Build the API payload from module params."""
    policy = {}
    for param in ("name", "incident_preference"):
        value = module.params.get(param)
        if value is not None:
            policy[param] = value
    return {"policy": policy}


def needs_update(current, desired_policy):
    """Compare current API state against desired params. Returns True if different."""
    for key, desired_val in desired_policy.items():
        if desired_val is None:
            continue
        current_val = current.get(key)
        if current_val != desired_val:
            return True
    return False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", default="present", choices=["present", "absent"]),
            policy_id=dict(type="str"),
            name=dict(type="str"),
            incident_preference=dict(
                type="str",
                choices=["PER_POLICY", "PER_CONDITION", "PER_CONDITION_AND_TARGET"],
            ),
            host=dict(type="str", required=True),
            api_key=dict(type="str", no_log=True),
            validate_certs=dict(type="bool", default=True),
        ),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("policy_id",)),
            ("state", "present", ("name",)),
        ],
    )

    if not HAS_CLIENT:
        module.fail_json(msg="Required library 'requests' is not installed.")

    client = ApiClient(module)
    state = module.params["state"]

    current = get_current_state(client, module)
    payload = build_payload(module)
    desired_policy = payload["policy"]

    if state == "present":
        if current:
            if needs_update(current, desired_policy):
                resource_id = current.get("id", module.params.get("policy_id", ""))
                diff = {"before": current, "after": desired_policy}
                if module.check_mode:
                    module.exit_json(changed=True, alert_policy=current, diff=diff)
                result = client.update("alert_policy", resource_id, payload)
                module.exit_json(changed=True, alert_policy=result, diff=diff)
            else:
                module.exit_json(changed=False, alert_policy=current)
        else:
            if module.check_mode:
                module.exit_json(changed=True, diff={"before": {}, "after": desired_policy})
            result = client.create("alert_policy", payload)
            module.exit_json(changed=True, alert_policy=result,
                             diff={"before": {}, "after": desired_policy})
    else:
        if not current:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True, diff={"before": current, "after": {}})
        client.delete("alert_policy", module.params["policy_id"])
        module.exit_json(changed=True, diff={"before": current, "after": {}})


if __name__ == "__main__":
    main()
