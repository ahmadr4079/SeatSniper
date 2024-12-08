import os

from django.core.wsgi import get_wsgi_application

from seas.project.config import RunEnvType, seas_config

settings = 'seas.project.settings_production'
if seas_config.run_env_type == RunEnvType.development:
    settings = 'seas.project.settings_development'
elif seas_config.run_env_type == RunEnvType.stage:
    settings = "seas.project.settings_stage"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

application = get_wsgi_application()
