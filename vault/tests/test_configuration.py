from unittest import TestCase

from vault import config


class ConfigParsingTest(TestCase):
    def test_config_defaults(self):
        defaults = {
            "VAULTPY_ENABLE_VAULT": False,
            "VAULTPY_SECRETS_PATH": "/vault/secrets/secrets",
            "VAULTPY_ENABLE_DATADOG": True,
        }

        for setting, default in defaults.items():
            actual_setting = getattr(config, setting.replace("VAULTPY_", ""))
            self.assertEqual(
                actual_setting,
                default,
                f"{setting} should be `{default}` but was `{actual_setting}`",
            )
