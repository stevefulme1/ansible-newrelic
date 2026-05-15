# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added

- 50 modules covering full New Relic platform API
- CRUD + info module for every resource type
- EDA source plugins for event-driven automation
- Unit tests and CI pipeline

## [1.0.0-initial] - 2026-05-15

### Added

- Initial release of stevefulme1.newrelic collection
- Alert management modules:
  - `newrelic_alert_policy` - CRUD operations for alert policies
  - `newrelic_alert_policy_info` - Query alert policies
  - `newrelic_alert_condition` - Manage NRQL alert conditions
  - `newrelic_alert_condition_info` - Query alert conditions
- Dashboard management modules:
  - `newrelic_dashboard` - CRUD operations for dashboards
  - `newrelic_dashboard_info` - Query dashboards
- Synthetic monitoring modules:
  - `newrelic_synthetic_monitor` - Manage synthetic monitors
  - `newrelic_synthetic_monitor_info` - Query synthetic monitors
- Workload management modules:
  - `newrelic_workload` - Manage workloads
  - `newrelic_workload_info` - Query workloads
- Service level management modules:
  - `newrelic_service_level` - Manage SLI/SLO definitions
  - `newrelic_service_level_info` - Query service levels
- Query execution module:
  - `newrelic_nrql_query` - Execute NRQL queries
- Module utils:
  - `newrelic_api` - NerdGraph GraphQL client
- Doc fragments:
  - `newrelic_auth` - Shared authentication documentation
- EDA plugins:
  - `webhook` event source - Receive New Relic Workflow webhooks
  - `alerts` event source - Poll NerdGraph for alert violations
- Example EDA rulebooks:
  - `alert_remediation.yml` - Auto-remediation patterns
  - `slo_response.yml` - SLO breach response
- Comprehensive documentation and examples
- Unit tests for core modules
- CI/CD pipeline with lint, sanity, and unit tests

[1.0.0]: https://github.com/stevefulme1/ansible-newrelic/releases/tag/v1.0.0
