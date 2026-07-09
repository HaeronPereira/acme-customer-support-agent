from authlib.integrations.requests_client import OAuth2Session
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
REALM = os.getenv("KEYCLOAK_REALM")
SERVER = os.getenv("KEYCLOAK_SERVER")

AUTH_URL = (
    f"{SERVER}/realms/{REALM}"
    "/protocol/openid-connect/auth"
)

TOKEN_URL = (
    f"{SERVER}/realms/{REALM}"
    "/protocol/openid-connect/token"
)

REDIRECT_URI = "http://localhost:8501"