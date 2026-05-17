"""Normalize New Relic webhook payloads into a flat event structure.

Flattens nested New Relic alert/incident webhook payloads so downstream
rules can match on simple top-level keys rather than navigating nested
JSON structures.
"""

DOCUMENTATION = r"""
---
event_filter: normalize
short_description: Flatten New Relic webhook payloads
description:
  - Normalizes nested New Relic alert/incident webhook payloads into a
    flat key-value structure suitable for EDA rule matching.
  - Extracts key fields from nested objects (condition, entity, policy).
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
options:
  include_raw:
    description: Whether to include the original raw payload under a C(raw) key.
    type: bool
    default: false
  prefix:
    description: Prefix to prepend to extracted keys.
    type: str
    default: ""
"""

EXAMPLES = r"""
- stevefulme1.newrelic.normalize:
    include_raw: false
"""


def main(event, include_raw=False, prefix=""):
    """Flatten a New Relic webhook payload."""
    if not isinstance(event, dict):
        return event

    payload = event.get("payload", event)
    result = {}

    # Direct top-level fields
    for key in ("event_type", "account_id", "account_name", "severity",
                "timestamp", "current_state", "details", "incident_id",
                "incident_url", "policy_name", "policy_url"):
        if key in payload:
            result[prefix + key] = payload[key]

    # Flatten condition block
    condition = payload.get("condition", {})
    if isinstance(condition, dict):
        for k, v in condition.items():
            result[prefix + "condition_" + k] = v

    # Flatten entity block
    entity = payload.get("targets", payload.get("entity", {}))
    if isinstance(entity, list) and entity:
        entity = entity[0]
    if isinstance(entity, dict):
        for k, v in entity.items():
            result[prefix + "entity_" + k] = v

    if include_raw:
        result["raw"] = event

    # Preserve meta keys from the EDA framework
    for key in ("meta", "source"):
        if key in event:
            result[key] = event[key]

    return result
