from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime

from config.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)
from config.sp_caller import exec_sp_one
from presentation.schemas.auth_schemas import (
    LoginRequest, RegisterRequest,
    ChangePasswordRequest, TokenResponse, RefreshRequest, ResetPasswordRequest
)


class AuthService:

    # ------------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------------
    @staticmethod
    async def login(payload: LoginRequest, db: AsyncSession) -> TokenResponse:

        auth_data = await exec_sp_one(db, "SP_Auth_GetHashOnly", {
            "UserName": payload.username
        })

        if not auth_data or not auth_data["Active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        AuthService._check_lockout(auth_data)

        password_valid = verify_password(payload.password, auth_data["UserPass"])
        auth_data["UserPass"] = None

        if not password_valid:
            result = await exec_sp_one(db, "SP_Auth_LoginFailed", {
                "UserName": payload.username,
                "MaxAttempts": 5,
                "LockDurationMin": 15
            })
            await db.commit()

            if result and result.get("LockoutEnd"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account locked for 15 minutes due to too many failed attempts"
                )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        user = await exec_sp_one(db, "SP_Auth_LoginSuccess", {
            "UserName": payload.username
        })
        await db.commit()

        return AuthService._build_token_response(user)

    # ------------------------------------------------------------------
    # REGISTER
    # ------------------------------------------------------------------
    @staticmethod
    async def register(payload: RegisterRequest, db: AsyncSession) -> dict:

        hashed = hash_password(payload.password)

        result = await exec_sp_one(db, "SP_Auth_RegisterUser", {
            "UserName": payload.username,
            "PasswordHash": hashed,
            "OfficerName": payload.officer_name,
            "EmailID": payload.email_id,
            "Mobile": payload.mobile,
            "RoleID": payload.role_id
        })
        await db.commit()

        hashed = None

        if not result or result.get("Success") == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )

        return {
            "message": "User registered successfully",
            "id": result["NewAutoID"]
        }

    # ------------------------------------------------------------------
    # CHANGE PASSWORD
    # ------------------------------------------------------------------
    @staticmethod
    async def change_password(
        payload: ChangePasswordRequest,
        current_user_id: str,
        db: AsyncSession
    ) -> dict:

        auth_data = await exec_sp_one(db, "SP_Auth_GetHashOnly", {
            "UserName": current_user_id
        })

        if not auth_data or not auth_data["Active"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not verify_password(payload.current_password, auth_data["UserPass"]):
            auth_data["UserPass"] = None
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )

        auth_data["UserPass"] = None

        temp_auth = await exec_sp_one(db, "SP_Auth_GetHashOnly", {
            "UserName": current_user_id
        })

        is_same = verify_password(payload.new_password, temp_auth["UserPass"])
        temp_auth["UserPass"] = None

        if is_same:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from current password"
            )

        new_hashed = hash_password(payload.new_password)

        result = await exec_sp_one(db, "SP_Auth_ChangePassword", {
            "UserName": current_user_id,
            "NewHashedPass": new_hashed
        })
        await db.commit()

        new_hashed = None

        if not result or result.get("Success") == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or inactive"
            )

        return {"message": "Password changed successfully"}

    # ------------------------------------------------------------------
    # REFRESH TOKEN
    # ------------------------------------------------------------------
    @staticmethod
    async def refresh(payload: RefreshRequest, db: AsyncSession) -> TokenResponse:

        try:
            data = decode_token(payload.refresh_token)
            if data.get("type") != "refresh":
                raise ValueError("Not a refresh token")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        user = await exec_sp_one(db, "SP_Auth_GetUserByID", {
            "UserName": data.get("sub")
        })

        if not user or not user["Active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        AuthService._check_lockout(user)

        return AuthService._build_token_response(user)

    # ------------------------------------------------------------------
    # UNLOCK USER
    # ------------------------------------------------------------------
    @staticmethod
    async def unlock_user(target_user_id: str, db: AsyncSession) -> dict:

        result = await exec_sp_one(db, "SP_Auth_UnlockUser", {
            "UserName": target_user_id
        })
        await db.commit()

        if not result or result.get("Success") == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {"message": f"User {target_user_id} unlocked successfully"}

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    @staticmethod
    def _check_lockout(auth_data: dict):
        if auth_data.get("LockoutEnabled") and auth_data.get("LockoutEnd"):
            lockout_end = auth_data["LockoutEnd"]
            if isinstance(lockout_end, str):
                lockout_end = datetime.fromisoformat(lockout_end)
            if lockout_end > datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Account locked until {lockout_end.strftime('%Y-%m-%d %H:%M:%S')} UTC"
                )

    @staticmethod
    def _build_token_response(user: dict) -> TokenResponse:
        token_payload = {
            "sub": user["UserName"],
            "role_id": user["RoleID"],
            "role_name": user["User_Role"],
            # "office_code": user["Office_Code"],
            "uuid_id": user["Uuid_ID"],
        }
        return TokenResponse(
            access_token=create_access_token(token_payload),
            refresh_token=create_refresh_token(token_payload),
            role=user["User_Role"],
            # office_code=user["Office_Code"],
        )
    
    @staticmethod
    async def reset_password(payload: ResetPasswordRequest, db: AsyncSession) -> dict:

        # Step 1: Hash new password in service layer
        # Plain password never reaches DB or SP
        new_hashed = hash_password(payload.new_password)

        # Step 2: SP verifies username + mobile match, then updates hash
        result = await exec_sp_one(db, "SP_Auth_ResetPassword", {
            "UserName":      payload.username,
            "Mobile":      payload.mobile,
            "NewHashPass": new_hashed
        })
        await db.commit()

        new_hashed = None  # clear immediately after SP call

        # Step 3: SP returns INVALID_CREDENTIALS for both
        # wrong username AND wrong mobile — prevents user enumeration
        if not result or result["Success"] == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or mobile number"
            )

        return {"message": "Password reset successfully"}