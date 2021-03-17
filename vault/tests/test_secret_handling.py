from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from vault.tests.data import de_test_secrets
from vault.tests.helpers import override_env

TEST_DATA_PATH = Path.cwd().joinpath("data")
TEST_SECRET = "shhhhh!"


class SecretLoaderTest(TestCase):
    @override_env({"VAULTPY_ENABLE_VAULT": "false", "VAULTPY_ENABLE_DATADOG": "false"})
    @patch("vault.import_module")
    def test_de_secrets_module(self, mock_import):
        from vault import secrets

        mock_import.return_value = de_test_secrets
        self.assertEqual(TEST_SECRET, secrets.SUPER_SECRET_KEY)

    @override_env(
        {
            "VAULTPY_ENABLE_VAULT": "true",
            "VAULTPY_ENABLE_DATADOG": "false",
            "VAULTPY_SECRETS_PATH": str(TEST_DATA_PATH.joinpath("secrets_json")),
        }
    )
    def test_json_secrets(self):
        from vault import secrets

        self.assertEqual(TEST_SECRET, secrets.SUPER_SECRET_KEY)

    @override_env(
        {
            "VAULTPY_ENABLE_VAULT": "true",
            "VAULTPY_ENABLE_DATADOG": "false",
            "VAULTPY_SECRETS_PATH": str(TEST_DATA_PATH.joinpath("secrets_json_base64")),
        }
    )
    def test_json_base64_secrets(self):
        from vault import secrets

        self.assertEqual(TEST_SECRET, secrets.SUPER_SECRET_KEY)
