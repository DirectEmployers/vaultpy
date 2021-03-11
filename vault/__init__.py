import logging
from base64 import b64decode, b64encode
from importlib import import_module
from json import loads
from typing import Dict

from datadog import statsd

import config

logger = logging.getLogger(__name__)


def _is_base64(s):
    """
    Checks whether a sting has been base 64 encoded.
    """
    try:
        return b64encode(b64decode(s)) == bytes(s, "utf-8")
    except Exception:
        return False


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
    with open(config.SECRETS_PATH) as file:
        contents = file.read().strip()

    if _is_base64(contents):
        contents = b64decode(contents)

    contents = loads(contents)

    try:
        # If the injected secret is formatted as a Vault Secret struct,
        # the actual secrets will be nested under two `data` keys.
        contents = contents["data"]
        contents = contents["data"]
    except KeyError:
        pass

    return contents


def _get_secrets() -> Dict:
    """
    Get secrets from de_secrets.py in local dev, or from Vault injected secrets file
    located at path in VAULT_SECRETS_PATH. Performs base 64 decode followed by JSON
    decode on file contents.
    """
    if not config.ENABLE_VAULT:
        # Use dev secrets when available.
        return _load_de_secrets()

    return _load_vault_secrets()


class VaultSecretsWrapper:
    """
    Provide access to secrets as attributes and send secret-usage analytics to Datadog.
    """

    def __init__(self, secrets: Dict):
        self._keys = secrets.keys()

        for key, value in secrets.items():
            # Set baseline usage of 0 for all secrets.
            self._record_usage(key)
            # Store secrets as class
            setattr(self, key, value)

    def _record_usage(self, key, value=0):
        """
        Report secret usage to Datadog for evaluation and cleanup of old secrets.
        """
        if config.ENABLE_DATADOG:
            try:
                statsd.increment(
                    "vault.secrets.usage",
                    value=value,
                    tags=[f"secret_key:{key}"],
                )
            except Exception:
                logger.error("Vault secret usage could not be reported to Datadog!")
                config.ENABLE_DATADOG = False

    def __getattribute__(self, key: str):
        """
        Override the default getattribute method so that we can track secret key
        usage with Datadog. Non-secret attributes are passed on to the default method.
        """
        if key != "_keys" and key in self._keys:
            try:
                self._record_usage(key, 1)
                return super().__getattribute__(key)
            except AttributeError as error:
                logger.error(f"Requested secret could not be loaded: {key}")
                raise error

        return super().__getattribute__(key)


secrets = VaultSecretsWrapper(_get_secrets())
__all__ = ("secrets",)
