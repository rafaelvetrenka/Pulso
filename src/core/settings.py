import os


def get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


SERVICE_NAME = get_env("PULSO_SERVICE_NAME", "pulso")
APP_VERSION = get_env("PULSO_APP_VERSION", "0.1.0")

# Se vazio, API fica aberta (modo dev). Se preenchido, exige header X-API-Key.
API_KEY = get_env("PULSO_API_KEY", "")
