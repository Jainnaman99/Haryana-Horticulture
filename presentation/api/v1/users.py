from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import get_session
from application.services.user.query.user_query_service import UserQueryService
from application.services.user.dto.user_dto import UserDTO, UserCreate, UserUpdate, UserResponse
from application.dependencies.user.query.user_query_dependencies import get_user_query_service
from uuid import UUID
from application.services.user.command.user_command_service import UserCommandService
from application.dependencies.user.command.user_command_dependencies import get_user_command_service


router = APIRouter(prefix="/users", tags=["Users"])

# @router.get("/", response_model=List[UserDTO])
# async def get_users(service: UserQueryService = Depends(get_user_query_service)):
    
#     return await service.get_all_users()

@router.get("/", response_model=List[UserResponse])
async def get_all_users(service: UserQueryService = Depends(get_user_query_service)):
    return await service.get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, service: UserQueryService = Depends(get_user_query_service)):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
async def create_user(request: UserCreate, service: UserCommandService = Depends(get_user_command_service)):
    return await service.create_user(request)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, request: UserUpdate, service: UserCommandService = Depends(get_user_command_service)):
    # user = service.update_user(user_id, request.model_dump(exclude_unset=True))
    user = await service.update_user(user_id, request.model_dump(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: UUID, service: UserCommandService = Depends(get_user_command_service)):
    user = await service.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}