import os
from typing import Dict


def override_env(envs: Dict):
    def decorator(func):
        def wrapper(*args, **kwargs):
            restore_envs = {}

            for env, new_val in envs.items():
                if env in os.environ.keys():
                    restore_envs[env] = os.environ.get(env)
                os.environ[env] = new_val

            result = func(*args, **kwargs)

            for env in envs.keys():
                if env in restore_envs:
                    os.environ[env] = restore_envs[env]
                else:
                    del os.environ[env]

            return result

        return wrapper

    return decorator
