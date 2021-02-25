import logging
from base64 import b64decode
from importlib import import_module
from json import loads
from os import environ
from typing import Dict

from datadog import statsd

logger = logging.getLogger(__name__)


def _load_de_secrets() -> Dict:
    """
    Imports de_secrets module and returns a dictionary of its attributes.
    """
    de_secrets = import_module("de_secrets")
    return {k: getattr(de_secrets, k) for k in dir(de_secrets) if not k.startswith("_")}


def _load_vault_secrets() -> Dict:
    """
    Load Vault injected secrets file located at VAULT_SECRETS_PATH, then perform
    base 64 decode followed by JSON decode on file contents. This function
    should not be called anywhere except within this module!
    """
    with open(environ["VAULT_SECRETS_PATH"]) as file:
        contents = file.read()

    json_secrets = b64decode(contents)
    return loads(json_secrets)


def _get_secrets() -> Dict:
    """
    Get secrets from de_secrets.py in local dev, or from Vault injected secrets file
    located at path in VAULT_SECRETS_PATH. Performs base 64 decode followed by JSON
    decode on file contents.
    """
    if not environ.get("USE_VAULT"):
        # Use dev secrets when available.
        return _load_de_secrets()

    return _load_vault_secrets()


class VaultSecretsWrapper:
    """
    Provide access to secrets as attributes and send secret-usage analytics to Datadog.
    """

    def __init__(self, secrets: Dict):
        self._keys = secrets.keys()
        self._env = environ.get("DD_ENV")

        for key, value in secrets.items():
            statsd.increment(
                "vault.secrets.access_count",
                value=1,
                tags=[f"env:{self._env}", f"secret_key:{key}"],
            )
            setattr(self, key, value)

    def __getattribute__(self, key: str):
        """
        Override the default getattribute method so that we can track secret key
        usage with Datadog. Non-secret attributes are passed on to the default method.
        """
        if key not in ["_keys", "_env"] and key in self._keys:
            try:
                statsd.increment(
                    "vault.secrets.access_count",
                    value=1,
                    tags=[f"env:{self._env}", f"secret_key:{key}"],
                )
                return super().__getattribute__(key)
            except AttributeError as error:
                logger.error(f"Requested secret could not be loaded: {key}")
                raise error

        return super().__getattribute__(key)


secrets = VaultSecretsWrapper(_get_secrets())
__all__ = ("secrets",)
