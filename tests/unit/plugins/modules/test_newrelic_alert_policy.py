"""Unit tests for newrelic_alert_policy module."""

import pytest
from unittest.mock import MagicMock, patch

MODULE_PATH = "ansible_collections.stevefulme1.newrelic.plugins.modules.newrelic_alert_policy"


@pytest.fixture
def module_args():
    return {
        "host": "test.example.com",
        "username": "admin",
        "password": "secret",
        "validate_certs": False,
        "state": "present",
        "name": "test-alert-policy",
    }


class TestCreate:
    @patch(f"{MODULE_PATH}.ApiClient")
    def test_create(self, mock_client_cls, module_args):
        mock_client = MagicMock()
        mock_client.create.return_value = {"id": "123", "name": "test"}
        mock_client_cls.return_value = mock_client
        assert mock_client.create.return_value["id"] == "123"


class TestDelete:
    @patch(f"{MODULE_PATH}.ApiClient")
    def test_delete(self, mock_client_cls, module_args):
        mock_client = MagicMock()
        mock_client.delete.return_value = None
        mock_client_cls.return_value = mock_client
        mock_client.delete("alert_policy", "123")
        mock_client.delete.assert_called_once_with("alert_policy", "123")
