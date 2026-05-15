# Ansible Collection - stevefulme1.newrelic

Ansible collection for New Relic management via NerdGraph API and Event-Driven Automation.

This collection fills the gap in the New Relic ecosystem — while agent deployment roles exist, comprehensive management modules for alerts, dashboards, synthetics, SLOs, and workloads via NerdGraph have been missing. This collection provides full lifecycle management of New Relic resources through Ansible automation.

## Features

- **NerdGraph API Integration**: All modules use New Relic's GraphQL API (NerdGraph) for modern, efficient resource management
- **Comprehensive Module Coverage**: Alert policies, NRQL conditions, dashboards, synthetic monitors, workloads, and service levels
- **Event-Driven Automation**: EDA plugins for webhook receivers and alert polling
- **Info Modules**: Dedicated `*_info` modules for querying existing resources
- **Multi-Region Support**: Works with both US and EU New Relic regions

## Installation

```bash
ansible-galaxy collection install stevefulme1.newrelic
```

## Requirements

- Ansible >= 2.16.0
- Python >= 3.11
- Python packages:
  - requests >= 2.25.0

## Authentication

All modules require a New Relic User API Key. Set the `api_key` parameter or use the `NEW_RELIC_API_KEY` environment variable:

```bash
export NEW_RELIC_API_KEY="your_user_api_key_here"
```

You can generate a User API Key from your New Relic account at: **Account Settings → API Keys → User Keys**

## Modules

### Alert Management

- `newrelic_alert_policy` - Create, update, or delete alert policies
- `newrelic_alert_policy_info` - Query alert policies
- `newrelic_alert_condition` - Manage NRQL alert conditions
- `newrelic_alert_condition_info` - Query alert conditions

### Dashboard Management

- `newrelic_dashboard` - Create, update, or delete dashboards
- `newrelic_dashboard_info` - Query dashboards

### Synthetic Monitoring

- `newrelic_synthetic_monitor` - Manage synthetic monitors
- `newrelic_synthetic_monitor_info` - Query synthetic monitors

### Workload Management

- `newrelic_workload` - Manage workloads
- `newrelic_workload_info` - Query workloads

### Service Level Management

- `newrelic_service_level` - Manage SLI/SLO definitions
- `newrelic_service_level_info` - Query service levels

### Query Execution

- `newrelic_nrql_query` - Execute NRQL queries and return results

## EDA Plugins

### Event Sources

- `webhook` - Receive New Relic Workflow webhook notifications
- `alerts` - Poll NerdGraph for open alert violations

### Example Rulebooks

See `extensions/eda/rulebooks/` for example rulebooks:
- `alert_remediation.yml` - Auto-remediation based on alert webhooks
- `slo_response.yml` - SLO breach response automation

## Example Playbook

```yaml
---
- name: Manage New Relic resources
  hosts: localhost
  gather_facts: false
  vars:
    newrelic_account_id: 12345678
  
  tasks:
    - name: Create alert policy
      stevefulme1.newrelic.newrelic_alert_policy:
        api_key: "{{ lookup('env', 'NEW_RELIC_API_KEY') }}"
        account_id: "{{ newrelic_account_id }}"
        name: "Production API Alerts"
        incident_preference: PER_CONDITION
        state: present
      register: policy
    
    - name: Create NRQL alert condition
      stevefulme1.newrelic.newrelic_alert_condition:
        api_key: "{{ lookup('env', 'NEW_RELIC_API_KEY') }}"
        account_id: "{{ newrelic_account_id }}"
        policy_id: "{{ policy.policy.id }}"
        name: "High Error Rate"
        nrql:
          query: "SELECT percentage(count(*), WHERE error IS true) FROM Transaction"
        critical:
          threshold: 5
          threshold_duration: 300
          operator: ABOVE
        state: present
    
    - name: Query existing dashboards
      stevefulme1.newrelic.newrelic_dashboard_info:
        api_key: "{{ lookup('env', 'NEW_RELIC_API_KEY') }}"
        account_id: "{{ newrelic_account_id }}"
        name: "Production Overview"
      register: dashboards
    
    - name: Execute NRQL query
      stevefulme1.newrelic.newrelic_nrql_query:
        api_key: "{{ lookup('env', 'NEW_RELIC_API_KEY') }}"
        account_id: "{{ newrelic_account_id }}"
        query: "SELECT count(*) FROM Transaction SINCE 1 hour ago"
      register: query_result
```

## Testing

```bash
# Run unit tests
pytest tests/unit

# Run sanity tests
ansible-test sanity --docker

# Run integration tests (requires NEW_RELIC_API_KEY)
ansible-test integration --docker
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines.

## Security

See [SECURITY.md](SECURITY.md) for security policy and vulnerability reporting.

## License

Apache License 2.0

See [LICENSE](LICENSE) for full license text.

## Author

Steve Fulmer (sfulmer@redhat.com)

## Links

- [GitHub Repository](https://github.com/stevefulme1/ansible-newrelic)
- [New Relic NerdGraph Documentation](https://docs.newrelic.com/docs/apis/nerdgraph/get-started/introduction-new-relic-nerdgraph/)
- [Ansible Galaxy](https://galaxy.ansible.com/stevefulme1/newrelic)
