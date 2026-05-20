# -*- coding: utf-8 -*-
# Copyright 2026 Steve Fulmer
# Apache-2.0 (see LICENSE)

"""New Relic API client supporting REST v2, NerdGraph, and Synthetics v3."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

IMPORT_ERRORS = []
try:
    import requests
    HAS_REQUESTS = True
except ImportError as e:
    HAS_REQUESTS = False
    IMPORT_ERRORS.append(e)


# Resource endpoint mapping for real New Relic APIs
RESOURCE_ENDPOINTS = {
    "alert_policy": {
        "api": "rest",
        "base": "/v2/alerts_policies.json",
        "item": "/v2/alerts_policies/{id}.json",
        "id_field": "id",
        "list_key": "policies",
    },
    "dashboard": {
        "api": "nerdgraph",
        "id_field": "guid",
    },
    "synthetic_monitor": {
        "api": "synthetics",
        "base": "/v3/monitors",
        "item": "/v3/monitors/{id}",
        "id_field": "id",
        "list_key": "monitors",
    },
}

# NerdGraph mutations and queries for dashboards
NERDGRAPH_QUERIES = {
    "dashboard_get": """
        query($guid: EntityGuid!) {
          actor {
            entity(guid: $guid) {
              ... on DashboardEntity {
                guid
                name
                description
                permissions
                pages {
                  name
                  widgets {
                    title
                    configuration { area { nrqlQueries { query } } }
                  }
                }
              }
            }
          }
        }
    """,
    "dashboard_list": """
        query($accountId: Int!) {
          actor {
            entitySearch(queryBuilder: {type: DASHBOARD}) {
              results {
                entities {
                  ... on DashboardEntityOutline {
                    guid
                    name
                    accountId
                  }
                }
              }
            }
          }
        }
    """,
    "dashboard_create": """
        mutation($accountId: Int!, $dashboard: DashboardInput!) {
          dashboardCreate(accountId: $accountId, dashboard: $dashboard) {
            entityResult {
              guid
              name
            }
            errors {
              description
              type
            }
          }
        }
    """,
    "dashboard_update": """
        mutation($guid: EntityGuid!, $dashboard: DashboardInput!) {
          dashboardUpdate(guid: $guid, dashboard: $dashboard) {
            entityResult {
              guid
              name
            }
            errors {
              description
              type
            }
          }
        }
    """,
    "dashboard_delete": """
        mutation($guid: EntityGuid!) {
          dashboardDelete(guid: $guid) {
            status
            errors {
              description
              type
            }
          }
        }
    """,
}


class ApiClient:
    """API client for New Relic (REST v2, NerdGraph, Synthetics v3)."""

    def __init__(self, module):
        self.module = module
        self.host = module.params["host"]
        self.validate_certs = module.params.get("validate_certs", True)
        self.session = requests.Session()
        self.session.verify = self.validate_certs
        self._authenticate()

    def _authenticate(self):
        api_key = self.module.params.get("api_key")
        if api_key:
            # New Relic uses Api-Key header for REST and NerdGraph
            self.session.headers["Api-Key"] = api_key
        self.session.headers["Content-Type"] = "application/json"

    def _rest_url(self, path):
        return "https://{host}{path}".format(host=self.host, path=path)

    def _nerdgraph_url(self):
        return "https://api.newrelic.com/graphql"

    def _synthetics_url(self, path):
        return "https://synthetics.newrelic.com/synthetics/api{path}".format(path=path)

    def _endpoint(self, resource_type):
        ep = RESOURCE_ENDPOINTS.get(resource_type)
        if not ep:
            self.module.fail_json(
                msg="Unknown resource type: {0}".format(resource_type)
            )
        return ep

    # ── REST v2 (alert_policy) ───────────────────────────────────────

    def get(self, resource_type, resource_id):
        """GET a single resource by ID. Returns None if 404."""
        ep = self._endpoint(resource_type)

        if ep["api"] == "nerdgraph":
            return self._nerdgraph_get(resource_id)
        if ep["api"] == "synthetics":
            url = self._synthetics_url(ep["item"].format(id=resource_id))
        else:
            url = self._rest_url(ep["item"].format(id=resource_id))

        resp = self.session.get(url)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()
        # REST v2 wraps in a singular key (e.g. {"policy": {...}})
        if ep.get("list_key") and ep["list_key"].rstrip("s") in data:
            return data[ep["list_key"].rstrip("s")]
        return data

    def list(self, resource_type, params=None):
        """List resources."""
        ep = self._endpoint(resource_type)

        if ep["api"] == "nerdgraph":
            return self._nerdgraph_list()
        if ep["api"] == "synthetics":
            url = self._synthetics_url(ep["base"])
        else:
            url = self._rest_url(ep["base"])

        resp = self.session.get(url, params=params or {})
        resp.raise_for_status()
        data = resp.json()
        return data.get(ep.get("list_key", "data"), [])

    def find_by_name(self, resource_type, name):
        """Find a resource by name. Returns first match or None."""
        items = self.list(resource_type)
        for item in items:
            if item.get("name") == name:
                return item
        return None

    def create(self, resource_type, payload):
        """Create a new resource."""
        ep = self._endpoint(resource_type)

        if ep["api"] == "nerdgraph":
            return self._nerdgraph_create(payload)
        if ep["api"] == "synthetics":
            url = self._synthetics_url(ep["base"])
        else:
            url = self._rest_url(ep["base"])

        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def update(self, resource_type, resource_id, payload):
        """Update an existing resource."""
        ep = self._endpoint(resource_type)

        if ep["api"] == "nerdgraph":
            return self._nerdgraph_update(resource_id, payload)
        if ep["api"] == "synthetics":
            url = self._synthetics_url(ep["item"].format(id=resource_id))
        else:
            url = self._rest_url(ep["item"].format(id=resource_id))

        resp = self.session.put(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def delete(self, resource_type, resource_id):
        """Delete a resource. Returns silently on 404."""
        ep = self._endpoint(resource_type)

        if ep["api"] == "nerdgraph":
            return self._nerdgraph_delete(resource_id)
        if ep["api"] == "synthetics":
            url = self._synthetics_url(ep["item"].format(id=resource_id))
        else:
            url = self._rest_url(ep["item"].format(id=resource_id))

        resp = self.session.delete(url)
        if resp.status_code == 404:
            return
        resp.raise_for_status()

    # ── NerdGraph (dashboard) ────────────────────────────────────────

    def _nerdgraph_query(self, query, variables=None):
        """Execute a NerdGraph query/mutation."""
        payload = {"query": query, "variables": variables or {}}
        resp = self.session.post(self._nerdgraph_url(), json=payload)
        resp.raise_for_status()
        data = resp.json()
        if "errors" in data and data["errors"]:
            self.module.fail_json(
                msg="NerdGraph error: {0}".format(json.dumps(data["errors"]))
            )
        return data.get("data", {})

    def _nerdgraph_get(self, guid):
        data = self._nerdgraph_query(
            NERDGRAPH_QUERIES["dashboard_get"], {"guid": guid}
        )
        entity = data.get("actor", {}).get("entity")
        return entity

    def _nerdgraph_list(self):
        data = self._nerdgraph_query(NERDGRAPH_QUERIES["dashboard_list"], {})
        results = (
            data.get("actor", {})
            .get("entitySearch", {})
            .get("results", {})
            .get("entities", [])
        )
        return results

    def _nerdgraph_create(self, payload):
        data = self._nerdgraph_query(
            NERDGRAPH_QUERIES["dashboard_create"],
            {"accountId": payload.get("account_id"), "dashboard": payload.get("dashboard", payload)},
        )
        result = data.get("dashboardCreate", {})
        errors = result.get("errors", [])
        if errors:
            self.module.fail_json(msg="Dashboard create failed: {0}".format(errors))
        return result.get("entityResult", {})

    def _nerdgraph_update(self, guid, payload):
        data = self._nerdgraph_query(
            NERDGRAPH_QUERIES["dashboard_update"],
            {"guid": guid, "dashboard": payload.get("dashboard", payload)},
        )
        result = data.get("dashboardUpdate", {})
        errors = result.get("errors", [])
        if errors:
            self.module.fail_json(msg="Dashboard update failed: {0}".format(errors))
        return result.get("entityResult", {})

    def _nerdgraph_delete(self, guid):
        data = self._nerdgraph_query(
            NERDGRAPH_QUERIES["dashboard_delete"], {"guid": guid}
        )
        result = data.get("dashboardDelete", {})
        errors = result.get("errors", [])
        if errors:
            self.module.fail_json(msg="Dashboard delete failed: {0}".format(errors))
