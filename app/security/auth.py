from enum import Enum
from typing import Optional, List
from fastapi import Header, HTTPException, status, Depends
from app.config import settings

class Role(str, Enum):
    ADMIN = "admin"
    ML_ENGINEER = "ml_engineer"
    VIEWER = "viewer"
    SERVICE = "service"

class User:
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role

def get_current_user(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> User:
    """
    Authenticate request via X-API-Key header.
    Conforms to SR-01: unauthenticated requests receive 401.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials. Provide X-API-Key header."
        )

    if x_api_key == settings.ADMIN_API_KEY:
        return User(username="admin_user", role=Role.ADMIN)
    elif x_api_key == settings.ML_ENGINEER_API_KEY:
        return User(username="ml_engineer_user", role=Role.ML_ENGINEER)
    elif x_api_key == settings.VIEWER_API_KEY:
        return User(username="viewer_user", role=Role.VIEWER)
    elif x_api_key == settings.SERVICE_API_KEY:
        return User(username="service_pipeline", role=Role.SERVICE)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials."
        )

def require_roles(allowed_roles: List[Role]):
    """
    Authorize user role.
    Conforms to SR-02: unauthorized roles receive 403.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: role '{current_user.role.value}' lacks required permissions."
            )
        return current_user
    return role_checker
