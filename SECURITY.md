# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this collection, please report it by emailing:

**sfulmer@redhat.com**

Please include the following information in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if available)

### What to Expect

- **Response Time**: You will receive an acknowledgment within 48 hours
- **Updates**: We will keep you informed of the progress toward fixing the vulnerability
- **Disclosure**: We will work with you to coordinate disclosure once a fix is available
- **Credit**: We will credit you for the discovery (unless you prefer to remain anonymous)

## Security Best Practices

When using this collection:

1. **API Key Management**
   - Never commit API keys to version control
   - Use Ansible Vault to encrypt sensitive credentials
   - Set API keys via environment variables or secure credential stores
   - Rotate API keys regularly

2. **Network Security**
   - Use HTTPS for all API communications (enforced by default)
   - Ensure proper firewall rules for EDA webhook receivers
   - Validate webhook signatures when receiving New Relic notifications

3. **Access Control**
   - Use New Relic User API Keys with minimal required permissions
   - Implement role-based access control in your Ansible automation
   - Audit automation runs and API access regularly

4. **Data Protection**
   - Be cautious with NRQL queries that may return sensitive data
   - Sanitize query results before logging or storing
   - Follow your organization's data retention policies

## Known Security Considerations

- **API Key Exposure**: Ensure `no_log: true` is used when handling API keys in playbooks
- **Webhook Authentication**: EDA webhook receiver should validate request signatures
- **NRQL Injection**: Always validate and sanitize user input before constructing NRQL queries

## Security Updates

Security updates will be released as patch versions and documented in the [CHANGELOG.md](CHANGELOG.md).
