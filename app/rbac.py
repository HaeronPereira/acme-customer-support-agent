from fastapi import HTTPException, status


def require_role(
    user: dict,
    allowed_roles: list[str],
):
    """
    Raise HTTP 403 if the authenticated user does not
    have one of the required roles.
    """

    roles = user.get("roles", [])

    if any(role in roles for role in allowed_roles):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to perform this action.",
    )