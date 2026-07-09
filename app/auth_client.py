import os

from authlib.integrations.httpx_client import OAuth2Client
from dotenv import load_dotenv

load_dotenv()

KEYCLOAK = os.getenv("KEYCLOAK_SERVER")
REALM = os.getenv("KEYCLOAK_REALM")

CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8501"

DISCOVERY_URL = (
    f"{KEYCLOAK}/realms/{REALM}"
    "/.well-known/openid-configuration"
)