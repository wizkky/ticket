"""Create private local configuration once, without overwriting existing files."""

import base64
import os
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local"
LOCAL.mkdir(exist_ok=True, mode=0o700)


def read_env(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return dict(
        line.split("=", 1)
        for line in path.read_text().splitlines()
        if line and not line.startswith("#") and "=" in line
    )


def write_new(path: Path, values: dict[str, str]) -> None:
    if path.exists():
        return
    with path.open("x") as stream:
        os.chmod(path, 0o600)
        stream.write("# Local development only. Generated once; do not commit.\n")
        stream.writelines(f"{key}={value}\n" for key, value in values.items())


api_path = ROOT / "apps/api/.env"
previous_api = read_env(api_path)
stack_path = LOCAL / "stack.env"
write_new(
    stack_path,
    {
        "DB_NAME": previous_api.get("DB_NAME", "caudaltickets"),
        "DB_USER": previous_api.get("DB_USER", "caudaltickets"),
        "DB_PASSWORD": previous_api.get("DB_PASSWORD", secrets.token_urlsafe(32)),
    },
)
db = read_env(stack_path)
write_new(
    api_path,
    {
        **db,
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "5432",
        "SECRET_KEY": secrets.token_urlsafe(64),
        "SALT_KEY": base64.urlsafe_b64encode(secrets.token_bytes(32)).decode(),
        "DEBUG": "True",
        "CAUDAL_DEMO": "True",
        "DEMO_MODE": "False",
        "SYSTEM_TESTING": "False",
        "ALLOWED_HOSTS": "localhost,127.0.0.1,testserver",
        "BASE_URL": "http://localhost:8000",
        "FRONTEND_BASE_URL": "http://localhost:5173",
        "SITE_NAME": "Caudal Creativo",
        "DEFAULT_TICKET_CURRENCY": "CLP",
        "FEATURE_ORGANIZATION_CREATION": "True",
        "FEATURE_MALWARE_SCAN": "False",
        "FEATURE_TELEGRAM": "False",
        "FEATURE_LLM_EVALUATION": "False",
        "FEATURE_OBSERVABILITY": "False",
        "CELERY_TASK_ALWAYS_EAGER": "True",
        "SILK_PROFILER": "False",
        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": "6379",
        "EMAIL_HOST": "127.0.0.1",
        "EMAIL_PORT": "1025",
        "EMAIL_HOST_USER": "",
        "EMAIL_HOST_PASSWORD": "",
        "EMAIL_USE_TLS": "False",
        "EMAIL_USE_SSL": "False",
        "DEFAULT_FROM_EMAIL": "Caudal Creativo <demo@caudaltickets.example.com>",
        "STRIPE_ACCOUNT": "",
        "STRIPE_SECRET_KEY": "",
        "STRIPE_WEBHOOK_SECRET": "",
    },
)
for key in db:
    if read_env(api_path).get(key) != db[key]:
        raise SystemExit(
            f"Configuration mismatch for {key}; align apps/api/.env with .local/stack.env without resetting your database."
        )
write_new(ROOT / "apps/web/.env", {"PUBLIC_API_URL": "http://localhost:8000"})
print(
    "Local configuration prepared; existing files preserved. No Stripe credentials configured by this script."
)
