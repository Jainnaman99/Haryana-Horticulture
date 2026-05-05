from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime



class UserDTO(BaseModel):
    UserId: Optional[int]
    Username: Optional[str]
    Email: Optional[EmailStr]
    PasswordHash: Optional[str]
    Role: Optional[str]

    LocationID: Optional[int] = None
    ApplicationGranted: Optional[str] = None
    ModulesGranted: Optional[str] = None
    dcode: Optional[str] = None
    tcode: Optional[str] = None
    SubDivCode: Optional[str] = None
    UserType: Optional[str] = None
    Status: Optional[str] = None

class UserCreate(BaseModel):
    Username: str
    Email: EmailStr
    Password: str   # 👈 plain password (hash it in service layer)
    Role: str
    LocationID: Optional[int] = None

class UserUpdate(BaseModel):
    Username: Optional[str] = None
    Email: Optional[EmailStr] = None
    Password: Optional[str] = None
    Role: Optional[str] = None
    LocationID: Optional[int] = None
    Status: Optional[str] = None
    

class UserResponse(BaseModel):
    UserId: int
    Username: str
    Email: EmailStr
    PasswordHash: str
    Role: str

    LocationID: Optional[int] = None
    ApplicationGranted: Optional[str] = None
    ModulesGranted: Optional[str] = None
    dcode: Optional[str] = None
    tcode: Optional[str] = None
    SubDivCode: Optional[str] = None
    UserType: Optional[str] = None
    Status: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True 
