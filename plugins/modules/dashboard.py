#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from New Relic NerdGraph API
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dashboard
short_description: Manage New Relic dashboards via NerdGraph
version_added: "1.0.0"
description:
  - Create, update, and delete dashboard resources.
  - Supports check mode and diff mode for safe operations.
author:
  - "Auto-generated from New Relic NerdGraph API"
options:
  state:
    description:
      - Desired state of the dashboard resource.
    type: str
    choices: ['present', 'absent']
    default: present

  name:
    description:
      - >-
        Dashboard name
    type: str

    required: true





  description:
    description:
      - >-
        Dashboard description
    type: str





  permissions:
    description:
      - >-
        Dashboard permissions
    type: str


    choices: ["PUBLIC_READ_ONLY", "PRIVATE"]




  pages:
    description:
      - >-
        List of dashboard page definitions
    type: list





extends_documentation_fragment:
  - stevefulme1.newrelic.auth
"""

EXAMPLES = r"""

- name: Create a dashboard
  stevefulme1.newrelic.dashboard:


    name: "example_name"








    state: present
  # API: POST /graphql



- name: Update a dashboard
  stevefulme1.newrelic.dashboard:
    guid: "existing_id"




    description: "updated_description"



    permissions: "updated_permissions"



    pages: "updated_pages"


    state: present
  # API:  



- name: Delete a dashboard
  stevefulme1.newrelic.dashboard:
    guid: "existing_id"
    state: absent
  # API: POST /graphql

"""

RETURN = r"""

guid:
  description: >-
    Dashboard GUID
  returned: success
  type: str


name:
  description: >-
    Dashboard name
  returned: success
  type: str


description:
  description: >-
    Dashboard description
  returned: success
  type: str


permissions:
  description: >-
    Dashboard permissions
  returned: success
  type: str


pages:
  description: >-
    Dashboard pages
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
    """Retrieve the current state of the dashboard via GET."""

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

    if module.params.get("description") is not None:
        payload["description"] = module.params["description"]

    if module.params.get("permissions") is not None:
        payload["permissions"] = module.params["permissions"]

    if module.params.get("pages") is not None:
        payload["pages"] = module.params["pages"]

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

            description=dict(
                type="str",





            ),

            permissions=dict(
                type="str",


                choices=['PUBLIC_READ_ONLY', 'PRIVATE'],




            ),

            pages=dict(
                type="list",





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

                result["description"] = current.get("description")

                result["permissions"] = current.get("permissions")

                result["pages"] = current.get("pages")


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
