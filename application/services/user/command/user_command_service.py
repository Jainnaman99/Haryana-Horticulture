import uuid
from domain.entities.user import User
from domain.interfaces.user.command.iuser_command_repository import IUserCommandRepository
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from application.services.user.dto.user_dto import UserCreate, UserResponse, UserUpdate

IST = ZoneInfo("Asia/Kolkata")

class UserCommandService:
    def __init__(self, user_repo: IUserCommandRepository):
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate) -> UserResponse:
        new_user = User(**user.model_dump())
        return await self.user_repo.create_user(new_user)

    async def update_user(self, user_id: UUID, request: UserUpdate):
        request["ModifiedOn"] = datetime.now(IST)
        return await self.user_repo.update_user(user_id, request)

    async def delete_user(self, user_id: UUID):
        return await self.user_repo.delete_user(user_id)
