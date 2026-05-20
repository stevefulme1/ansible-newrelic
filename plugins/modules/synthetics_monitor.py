#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from New Relic NerdGraph API
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: synthetics_monitor
short_description: Manage New Relic Synthetics monitors via NerdGraph
version_added: "1.0.0"
description:
  - Create, update, and delete synthetics_monitor resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Auto-generated from New Relic NerdGraph API"
options:
  state:
    description:
      - Desired state of the synthetics_monitor resource.
    type: str
    choices: ['present', 'absent']
    default: present

  name:
    description:
      - >-
        Monitor name
    type: str

    required: true





  monitor_type:
    description:
      - >-
        Monitor type
    type: str

    required: true


    choices: ["SIMPLE", "BROWSER", "SCRIPTED_BROWSER", "SCRIPTED_API"]




  uri:
    description:
      - >-
        URI to monitor
    type: str





  period:
    description:
      - >-
        Monitor frequency
    type: str


    choices: ["EVERY_MINUTE", "EVERY_5_MINUTES", "EVERY_10_MINUTES", "EVERY_15_MINUTES", "EVERY_30_MINUTES", "EVERY_HOUR", "EVERY_6_HOURS", "EVERY_12_HOURS", "EVERY_DAY"]




  locations:
    description:
      - >-
        List of public locations
    type: list





  status:
    description:
      - >-
        Monitor status
    type: str


    choices: ["ENABLED", "DISABLED", "MUTED"]




extends_documentation_fragment:
  - stevefulme1.newrelic.auth
"""

EXAMPLES = r"""

- name: Create a synthetics_monitor
  stevefulme1.newrelic.synthetics_monitor:


    name: "example_name"



    monitor_type: "example_monitor_type"










    state: present
  # API: POST /graphql



- name: Update a synthetics_monitor
  stevefulme1.newrelic.synthetics_monitor:
    guid: "existing_id"






    uri: "updated_uri"



    period: "updated_period"



    locations: "updated_locations"



    status: "updated_status"


    state: present
  # API:  



- name: Delete a synthetics_monitor
  stevefulme1.newrelic.synthetics_monitor:
    guid: "existing_id"
    state: absent
  # API: POST /graphql

"""

RETURN = r"""

guid:
  description: >-
    Monitor GUID
  returned: success
  type: str


name:
  description: >-
    Monitor name
  returned: success
  type: str


monitor_type:
  description: >-
    Monitor type
  returned: success
  type: str


uri:
  description: >-
    Monitored URI
  returned: success
  type: str


period:
  description: >-
    Check frequency
  returned: success
  type: str


status:
  description: >-
    Monitor status
  returned: success
  type: str


locations:
  description: >-
    Monitor locations
  returned: success
  type: list


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.newrelic.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def get_current_state(client, module):
    """Retrieve the current state of the synthetics_monitor via GET."""

    # No single-resource GET endpoint; fall back to list + filter
    identifier = module.params.get("guid")

    name = module.params.get("name")
    search_key = "name"
    search_value = name if identifier is None else identifier

    if search_value is None:
        return None
    try:
        items = client.get("/graphql")
        if isinstance(items, dict):
            items = items.get("results", items.get("data", items.get("items", [])))
        for item in items:
            if str(item.get(search_key)) == str(search_value):
                return item
            if str(item.get("guid")) == str(search_value):
                return item
        return None
    except ClientError:
        return None



def needs_update(current, desired):
    """Compare current state against desired params and return True if an update is needed."""
    if current is None:
        return True
    for key, value in desired.items():
        if value is None:
            continue
        current_value = current.get(key)
        if current_value != value:
            return True
    return False


def build_payload(module):
    """Build the API request payload from module params."""
    payload = {}

    if module.params.get("name") is not None:
        payload["name"] = module.params["name"]

    if module.params.get("monitor_type") is not None:
        payload["monitor_type"] = module.params["monitor_type"]

    if module.params.get("uri") is not None:
        payload["uri"] = module.params["uri"]

    if module.params.get("period") is not None:
        payload["period"] = module.params["period"]

    if module.params.get("locations") is not None:
        payload["locations"] = module.params["locations"]

    if module.params.get("status") is not None:
        payload["status"] = module.params["status"]

    return payload


def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),

            name=dict(
                type="str",

                required=True,





            ),

            monitor_type=dict(
                type="str",

                required=True,


                choices=['SIMPLE', 'BROWSER', 'SCRIPTED_BROWSER', 'SCRIPTED_API'],




            ),

            uri=dict(
                type="str",





            ),

            period=dict(
                type="str",


                choices=['EVERY_MINUTE', 'EVERY_5_MINUTES', 'EVERY_10_MINUTES', 'EVERY_15_MINUTES', 'EVERY_30_MINUTES', 'EVERY_HOUR', 'EVERY_6_HOURS', 'EVERY_12_HOURS', 'EVERY_DAY'],




            ),

            locations=dict(
                type="list",





            ),

            status=dict(
                type="str",


                choices=['ENABLED', 'DISABLED', 'MUTED'],




            ),

        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,

    )

    state = module.params["state"]
    result = dict(changed=False, diff=dict(before={}, after={}))

    try:
        client = Client(module)
        current = get_current_state(client, module)

        if state == "present":
            desired = build_payload(module)

            if current is None:
                # Resource does not exist — create it
                result["changed"] = True
                result["diff"]["before"] = {}
                result["diff"]["after"] = desired

                if not module.check_mode:

                    response = client.POST(
                        "/graphql",
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            elif needs_update(current, desired):
                # Resource exists but needs updating
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = dict(current, **{k: v for k, v in desired.items() if v is not None})

                if not module.check_mode:

                    identifier = current.get("guid")
                    path = "".replace(
                        "{guid}", str(identifier)
                    )
                    response = client.put(
                        path,
                        data=desired,
                    )
                    result.update(response if isinstance(response, dict) else {})


            else:
                # Resource exists and is up-to-date

                result["guid"] = current.get("guid")

                result["name"] = current.get("name")

                result["monitor_type"] = current.get("monitor_type")

                result["uri"] = current.get("uri")

                result["period"] = current.get("period")

                result["status"] = current.get("status")

                result["locations"] = current.get("locations")


        elif state == "absent":
            if current is not None:
                result["changed"] = True
                result["diff"]["before"] = current
                result["diff"]["after"] = {}

                if not module.check_mode:

                    identifier = current.get("guid")
                    path = "/graphql".replace(
                        "{guid}", str(identifier)
                    )
                    client.delete(path)


    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
