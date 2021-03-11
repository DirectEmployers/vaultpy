from os import environ


def parse_env_bool(env: str) -> bool:
    return env.casefold() in ["true", "1"]


# We're defaulting this to False until everything using vaultpy uses Vault.
# When True, vaultpy will attempt to retrieve and parse Vault agent injected secrets.
# When False vaultpy fallback on loading secrets from the de_secrets module.
# TODO: Remove USE_VAULT when all code has been updated to use VAULTPY_*
ENABLE_VAULT = parse_env_bool(
    environ.get("VAULTPY_ENABLE_VAULT", environ.get("USE_VAULT", "false"))
)

# Absolute path to get secrets from when VAULTPY_ENABLE_VAULT=true
# TODO: Remove VAULT_SECRETS_PATH when all code has been updated to use VAULTPY_*
SECRETS_PATH = environ.get(
    "VAULTPY_SECRETS_PATH", environ.get("VAULT_SECRETS_PATH", "/vault/secrets/secrets")
)

# Enable or disable reporting of secret usage to Datadog.
ENABLE_DATADOG = parse_env_bool(environ.get("VAULTPY_ENABLE_DATADOG", "true"))
