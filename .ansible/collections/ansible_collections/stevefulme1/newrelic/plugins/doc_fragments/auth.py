# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Steve Fulmer (@stevefulme1)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment:
    """Documentation fragment for stevefulme1.newrelic authentication."""

    DOCUMENTATION = r"""
options:

  api_key:
    description:
      - The New Relic User API key for NerdGraph authentication.
      - Can also be set via the C(NEW_RELIC_API_KEY) environment variable.
    type: str
    required: true

  account_id:
    description:
      - The New Relic account ID.
      - Can also be set via the C(NEW_RELIC_ACCOUNT_ID) environment variable.
    type: str
    required: false

  api_url:
    description:
      - The base URL of the New Relic NerdGraph API.
      - Override for New Relic EU region.
    type: str
    default: "https://api.newrelic.com/graphql"
  validate_certs:
    description:
      - Whether to validate SSL/TLS certificates when connecting to the API.
    type: bool
    default: true
  request_timeout:
    description:
      - Timeout in seconds for API requests.
    type: int
    default: 30
"""
