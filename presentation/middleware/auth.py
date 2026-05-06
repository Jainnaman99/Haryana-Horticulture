from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from datetime import datetime
from typing import List
from config.security import decode_token
from config.sp_caller import exec_sp_one
from presentation.schemas.auth_schemas import TokenData
from infrastructure.database.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession


security = HTTPBearer()


# ------------------------------------------------------------------
# STEP 1 — Decode & validate JWT token
# ------------------------------------------------------------------
def get_token_data(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Decodes Bearer token from Authorization header.
    Sync — no DB call, just JWT decode.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(credentials.credentials)

        if payload.get("type") != "access":
            raise credentials_exception

        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception

        return TokenData(
            user_id=user_id,
            role_id=payload.get("role_id"),
            role_name=payload.get("role_name"),
            office_code=payload.get("office_code"),
            uuid_id=payload.get("uuid_id"),
        )

    except JWTError:
        raise credentials_exception


# ------------------------------------------------------------------
# STEP 2 — Fetch live user from DB + enforce active & lockout
# ------------------------------------------------------------------
async def get_current_user(
    token_data: TokenData = Depends(get_token_data),
    db: AsyncSession = Depends(get_session)
) -> dict:
    """
    Async — fetches live user via SP_Auth_GetUserByID.
    Enforces Active status and lockout state.
    """
    user = await exec_sp_one(db, "SP_Auth_GetUserByID", {
        "UserName": token_data.user_id
    })

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user["Active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    if user.get("LockoutEnabled") and user.get("LockoutEnd"):
        lockout_end = user["LockoutEnd"]
        if isinstance(lockout_end, str):
            lockout_end = datetime.fromisoformat(lockout_end)
        if lockout_end > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account locked until {lockout_end.strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )

    return user


# ------------------------------------------------------------------
# STEP 3 — Role-based access control
# ------------------------------------------------------------------
def require_roles(allowed_roles: List[str]):
    """
    Factory for role-based route protection.

    Usage:
        # No current_user needed in route body
        @router.delete("/users/{id}", dependencies=[Depends(require_roles(["Admin"]))])

        # current_user needed in route body
        @router.get("/reports")
        def reports(current_user: dict = Depends(require_roles(["Admin", "Manager"]))):
    """
    async def role_checker(
        current_user: dict = Depends(get_current_user)
    ) -> dict:
        if current_user.get("User_Role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user

    return role_checker


# ------------------------------------------------------------------
# STEP 4 — Office-scoped access (optional utility)
# ------------------------------------------------------------------
async def require_same_office(
    target_office_code: int,
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Ensures user can only access data from their own office.
    Admins and SuperAdmins bypass this check.
    """
    is_admin = current_user.get("User_Role") in ["Admin", "SuperAdmin"]

    if not is_admin and current_user.get("Office_Code") != target_office_code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only access data from your own office"
        )

    return current_user