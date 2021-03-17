# Vaultpy
Parse injected [Vault](https://www.vaultproject.io/) secrets and track their usage with Datadog.

## Requirements
- Local Datadog agent
- Set [container annotations](https://www.vaultproject.io/docs/platform/k8s/injector/annotations) to inject Vault secrets in K8s

## Setup
For production, use the `VAULTPY_SECRETS_PATH` environment variable to set the path to the secrets that are injected by the Vault Agent in Kubernetes. This defaults to `/vault/secrets/secrets`. You will also need to set `VAULTPY_ENABLE_VAULT` (default `false`) to use injected secrets rather than loading them from a `de_secrets` module.

For local development, a `de_secrets.py` can be used to load secrets in a format not unlike Django settings.

Lastly you can toggle secret access tracking with Datadog via `VAULTPY_DATADOG_ENABLE`. This defaults to `true` because we want this in production, but it ought to be disabled in development environments.

## Usage
Import `vault.secrets` and then access the loaded secrets using by accessing dynamic properties loaded into the `secrets` object (i.e. `secrets.FOO`).

Example of usage in a settings file:
```python
from vault import secrets

FOO = secrets.FOO
BAR = getattr(secrets, "BAR", "")
BAZ = getattr(secrets, "BAZ")
```
