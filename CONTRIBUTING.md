# Contributing to ansible-newrelic

Thank you for your interest in contributing to the ansible-newrelic collection!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/ansible-newrelic.git`
3. Create a feature branch: `git checkout -b feature-name`
4. Install development dependencies: `pip install -r requirements.txt`

## Development Setup

### Prerequisites

- Python >= 3.11
- Ansible >= 2.16.0
- New Relic account with User API Key for testing

### Environment Setup

```bash
# Install collection in development mode
ansible-galaxy collection install -f .

# Install Python dependencies
pip install -r requirements.txt

# Set up test credentials
export NEW_RELIC_API_KEY="your_test_api_key"
export NEW_RELIC_ACCOUNT_ID="your_test_account_id"
```

## Code Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Maximum line length: 160 characters
- Use meaningful variable and function names

### Ansible Module Standards

- Follow [Ansible module development guidelines](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
- Include comprehensive documentation with examples
- Implement check mode support where applicable
- Return structured data with meaningful keys
- Use `module_utils` for shared code
- Follow idempotency principles

### Documentation

- All modules must include:
  - DOCUMENTATION block with parameters, return values, and examples
  - EXAMPLES block with realistic use cases
  - RETURN block documenting all return values
- Update CHANGELOG.md for all notable changes
- Update README.md if adding new features

## Testing

### Unit Tests

```bash
# Run all unit tests
pytest tests/unit -v

# Run specific test file
pytest tests/unit/plugins/modules/test_newrelic_alert_policy.py -v

# Run with coverage
pytest tests/unit --cov=plugins --cov-report=term-missing
```

### Sanity Tests

```bash
# Run all sanity tests
ansible-test sanity --docker

# Run specific test
ansible-test sanity --docker --test validate-modules
```

### Integration Tests

```bash
# Run integration tests (requires API credentials)
ansible-test integration --docker
```

### Linting

```bash
# Run ansible-lint
ansible-lint

# Run pylint
pylint plugins/
```

## Pull Request Process

1. **Create a Feature Branch**
   - Branch from `main`
   - Use descriptive branch names: `feature/add-entity-module`, `fix/condition-thresholds`

2. **Write Tests**
   - Add unit tests for new modules
   - Update existing tests if modifying functionality
   - Ensure all tests pass before submitting

3. **Update Documentation**
   - Add/update module documentation
   - Update CHANGELOG.md
   - Update README.md if adding new features

4. **Commit Guidelines**
   - Write clear, descriptive commit messages
   - Use present tense: "Add feature" not "Added feature"
   - Reference issues: "Fix #123: Resolve condition threshold bug"

5. **Submit Pull Request**
   - Fill out the PR template completely
   - Link to related issues
   - Ensure CI checks pass
   - Request review from maintainers

6. **Code Review**
   - Address review feedback promptly
   - Keep discussions focused and professional
   - Be open to suggestions and alternative approaches

## Adding New Modules

When adding a new module:

1. Create the module file in `plugins/modules/`
2. Create the corresponding info module if applicable
3. Add shared code to `plugins/module_utils/newrelic_api.py`
4. Write comprehensive unit tests in `tests/unit/plugins/modules/`
5. Add module to `meta/runtime.yml` action groups
6. Update documentation and examples
7. Add changelog entry

## Module Structure Template

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Steve Fulmer <sfulmer@redhat.com>
# Apache License 2.0 (see LICENSE or http://www.apache.org/licenses/LICENSE-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: newrelic_module_name
short_description: Brief description
description:
  - Detailed description
options:
  # Define all options
extends_documentation_fragment:
  - stevefulme1.newrelic.newrelic_auth
author:
  - Your Name (@github_username)
'''

EXAMPLES = r'''
# Examples here
'''

RETURN = r'''
# Return documentation here
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.newrelic.plugins.module_utils.newrelic_api import NewRelicAPI

def main():
    # Module implementation
    pass

if __name__ == '__main__':
    main()
```

## Reporting Issues

When reporting issues:

- Use the issue template
- Include collection version
- Provide minimal reproducible example
- Include error messages and logs
- Describe expected vs actual behavior

## Community Guidelines

- Be respectful and inclusive
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Help others in issues and discussions
- Share knowledge and best practices

## Questions?

- Open a [GitHub Discussion](https://github.com/stevefulme1/ansible-newrelic/discussions)
- Join the conversation in [GitHub Issues](https://github.com/stevefulme1/ansible-newrelic/issues)
- Email the maintainer: sfulmer@redhat.com

## License

By contributing to this project, you agree that your contributions will be licensed under the Apache License 2.0.
