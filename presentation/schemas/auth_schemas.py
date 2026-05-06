from pydantic import BaseModel, validator
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username:    str
    password:    str
    officer_name: str
    email_id:    str
    mobile:      str
    role_id:     int


    @validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Minimum 8 characters required")
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Must contain at least one special character")
        return v

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password:     str

    @validator("new_password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Minimum 8 characters required")
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain at least one digit")
        return v

class TokenResponse(BaseModel):
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"
    role:          str
    # office_code:   int

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    user_id:     Optional[str] = None
    role_id:     Optional[int] = None
    role_name:   Optional[str] = None
    office_code: Optional[int] = None
    uuid_id:     Optional[str] = None

class ResetPasswordRequest(BaseModel):
    username:     str
    mobile:       str
    new_password: str

    @validator("new_password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Minimum 8 characters required")
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain at least one digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Must contain at least one special character")
        return v

class ResetPasswordResponse(BaseModel):
    message: str