# Vaultpy
A module to parse injected [Vault](https://www.vaultproject.io/) secrets and track their usage with Datadog.

## Requirements
- Local Datadog agent
- Environment variables to access it
- Set [container annotations](https://www.vaultproject.io/docs/platform/k8s/injector/annotations) to inject Vault secrets in K8s

## Setup
For production, use the `VAULT_SECRETS_PATH` environment variable to set the path to the secrets that are injected by the Vault Agent in Kubernetes.

For local development, a `de_secrets.py` can be used to load secrets in a format not unlike Django settings.

## Usage
Import `vault.secrets` and then access the loaded secrets using by accessing dynamic properties loaded into the `secrets` object (i.e. `secrets.FOO`).

Example of usage in a settings file:
```python
from vault import secrets

FOO = secrets.FOO
BAR = getattr(secrets, "BAR", "")
BAZ = getattr(secrets, "BAZ")
```
