from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from vault.tests.data import de_test_secrets
from vault.tests.helpers import override_env
from vault import _parse_json_secrets

TEST_DATA_PATH = Path.cwd().joinpath("data")
TEST_SECRET = "shhhhh!"


class SecretLoaderTest(TestCase):
    @override_env({"VAULTPY_ENABLE_VAULT": "false", "VAULTPY_ENABLE_DATADOG": "false"})
    @patch("vault.import_module")
    def test_de_secrets_module(self, mock_import):
        """
        Test that vaultpy can get secrets from de_secrets.py when
        VAULTPY_ENABLE_VAULT is false. For testing purposes, de_secrets module is
        mocked from tests/data/de_test_secrets.py for this test.
        """
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
        """
        Test injected secrets that are JSON formatted.
        """
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
        """
        Test injected secrets that are JSON formatted and Base 64 encoded.
        """
        from vault import secrets

        self.assertEqual(TEST_SECRET, secrets.SUPER_SECRET_KEY)
