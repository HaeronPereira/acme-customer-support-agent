import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from keycloak import KeycloakOpenID

load_dotenv()

security = HTTPBearer()

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_SERVER"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    realm_name=os.getenv("KEYCLOAK_REALM"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
)

def get_public_key():

    return (
        "-----BEGIN PUBLIC KEY-----\n"
        + keycloak_openid.public_key()
        + "\n-----END PUBLIC KEY-----"
    )

ALGORITHM = "RS256"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Validate JWT issued by Keycloak.
    """

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            get_public_key(),
            algorithms=[ALGORITHM],
            options={
                "verify_aud": False,
            },
        )
        SYSTEM_ROLES = {
            "default-roles-acme",
            "offline_access",
            "uma_authorization",
        }
        user = {
                "id": payload.get("sub"),
                "username": payload.get("preferred_username"),
                "name": payload.get("name"),
                "email": payload.get("email"),
                "roles": [role for role in payload.get("realm_access", {}).get("roles", []) if role not in SYSTEM_ROLES
],
            }

        return user

    except JWTError as e:

        print(e)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    
def login(username: str, password: str):

    return keycloak_openid.token(
        username=username,
        password=password,
    )