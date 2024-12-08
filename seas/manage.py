#!/usr/bin/env python
import os
import sys

from seas.project.config import RunEnvType, seas_config


def main():
    settings = 'seas.project.settings_production'
    if seas_config.run_env_type == RunEnvType.development:
        settings = 'seas.project.settings_development'
    elif seas_config.run_env_type == RunEnvType.stage:
        settings = "seas.project.settings_stage"

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
