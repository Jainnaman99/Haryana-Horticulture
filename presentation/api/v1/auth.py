from fastapi import APIRouter, Depends
from infrastructure.database.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.auth.auth_service import AuthService
from presentation.middleware.auth import get_current_user, require_roles
from presentation.schemas.auth_schemas import (
    LoginRequest, RegisterRequest,
    ChangePasswordRequest, RefreshRequest, TokenResponse, ResetPasswordRequest, ResetPasswordResponse
)


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async  def login(payload: LoginRequest, db: AsyncSession = Depends(get_session)):
    return await AuthService.login(payload, db)

@router.post("/register")
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_session)):
    return await AuthService.register(payload, db)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_session)):
    return await AuthService.refresh(payload, db)

@router.post("/change-password")
async def change_password(
    payload: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    return await AuthService.change_password(payload, current_user["UserName"], db)

@router.post("/unlock/{user_id}", dependencies=[Depends(require_roles(["Admin", "SuperAdmin"]))])
async def unlock_user(user_id: str, db: AsyncSession = Depends(get_session)):
    return await AuthService.unlock_user(user_id, db)

@router.post("/reset-password",dependencies=[Depends(require_roles(["SuperAdmin"]))], response_model=ResetPasswordResponse)
async def reset_password(
    payload: ResetPasswordRequest,
    db: AsyncSession = Depends(get_session)
):
    return await AuthService.reset_password(payload, db)