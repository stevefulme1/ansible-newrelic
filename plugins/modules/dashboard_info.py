#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Auto-generated from New Relic NerdGraph API
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dashboard_info
short_description: Retrieve information about dashboard resources
version_added: "1.0.0"
description:
  - Retrieve a single dashboard by its identifier, or list all dashboard resources.
  - This module always reports C(changed=False).
author:
  - "Auto-generated from New Relic NerdGraph API"
options:
  guid:
    description:
      - The unique identifier of the dashboard to retrieve.
      - When omitted, all dashboard resources are listed.
    type: str
    required: false

  name:
    description:
      - Filter results by name.
    type: str
    required: false










  page:
    description:
      - Page number for paginated results.
      - Only applies when listing resources.
    type: int
    required: false
  page_size:
    description:
      - Number of results per page.
      - Only applies when listing resources.
    type: int
    required: false
extends_documentation_fragment:
  - stevefulme1.newrelic.auth
"""

EXAMPLES = r"""
- name: Get a specific dashboard
  stevefulme1.newrelic.dashboard_info:
    guid: "example_id"
  register: result

- name: List all dashboard resources
  stevefulme1.newrelic.dashboard_info:
  register: result


- name: List dashboard resources filtered by name
  stevefulme1.newrelic.dashboard_info:
    name: "my_dashboard"
  register: result


- name: List dashboard resources with pagination
  stevefulme1.newrelic.dashboard_info:
    page: 1
    page_size: 50
  register: result
"""

RETURN = r"""
dashboards:
  description: List of dashboard resources matching the query.
  returned: always
  type: list
  elements: dict
  contains:

    guid:
      description: >-
        Dashboard GUID
      type: str


    name:
      description: >-
        Dashboard name
      type: str


    description:
      description: >-
        Dashboard description
      type: str


    permissions:
      description: >-
        Dashboard permissions
      type: str


    pages:
      description: >-
        Dashboard pages
      type: list


"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.newrelic.plugins.module_utils.api_client import (
    Client,
    ClientError,
    argument_spec as auth_argument_spec,
)


def fetch_single(client, identifier):
    """Retrieve a single dashboard by identifier."""

    # No single-resource GET endpoint; filter from list
    items = client.get("/graphql")
    if isinstance(items, dict):
        items = items.get("results", items.get("data", items.get("items", [])))
    for item in items:
        if str(item.get("guid")) == str(identifier):
            return item
    return None



def fetch_list(client, module):
    """List dashboard resources with optional filtering and pagination."""

    params = {}


    name_filter = module.params.get("name")
    if name_filter is not None:
        params["name"] = name_filter












    page = module.params.get("page")
    page_size = module.params.get("page_size")

    if page is not None or page_size is not None:
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        response = client.get("/graphql", params=params)
        if isinstance(response, dict):
            return response.get("results", response.get("data", response.get("items", [])))
        return response if isinstance(response, list) else []
    else:
        return client.get_paginated("/graphql", params=params)



def main():
    spec = auth_argument_spec()
    spec.update(
        dict(
            guid=dict(type="str", required=False),

            name=dict(type="str", required=False),










            page=dict(type="int", required=False),
            page_size=dict(type="int", required=False),
        )
    )

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ("guid", "page"),
            ("guid", "page_size"),
        ],
    )

    result = dict(
        changed=False,
        dashboards=[],
    )

    try:
        client = Client(module)
        identifier = module.params.get("guid")

        if identifier is not None:
            item = fetch_single(client, identifier)
            result["dashboards"] = [item] if item else []
        else:
            result["dashboards"] = fetch_list(client, module)

    except ClientError as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
