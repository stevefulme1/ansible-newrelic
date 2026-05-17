"""Filter New Relic events by severity level."""

DOCUMENTATION = r"""
---
event_filter: severity
short_description: Filter New Relic events by severity
description:
  - Passes through only events matching the configured severity levels.
  - Supports New Relic severity values like CRITICAL, WARNING, INFO.
version_added: "1.0.0"
author: Steve Fulmer (@stevefulme1)
options:
  min_severity:
    description:
      - Minimum severity level to pass through.
      - Events below this level are dropped.
    type: str
    choices: [INFO, WARNING, CRITICAL]
    default: WARNING
  severity_key:
    description: Key in the event payload that contains the severity value.
    type: str
    default: severity
"""

EXAMPLES = r"""
- stevefulme1.newrelic.severity:
    min_severity: CRITICAL
"""

SEVERITY_ORDER = {"INFO": 0, "WARNING": 1, "CRITICAL": 2}


def main(event, min_severity="WARNING", severity_key="severity"):
    """Filter events by severity threshold."""
    if not isinstance(event, dict):
        return event

    payload = event.get("payload", event)
    event_severity = str(payload.get(severity_key, "")).upper()
    min_level = SEVERITY_ORDER.get(min_severity.upper(), 1)
    event_level = SEVERITY_ORDER.get(event_severity, -1)

    if event_level >= min_level:
        return event
    return None
