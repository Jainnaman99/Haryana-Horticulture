from uuid import UUID
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user import User
from application.services.user.dto.user_dto import UserCreate, UserUpdate, UserResponse
class IUserCommandRepository(ABC):

    @abstractmethod
    async def create_user(self, user: UserCreate) -> UserResponse: pass

    @abstractmethod
    async def update_user(self, updated_data: UserUpdate) -> Optional[UserResponse]: pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> Optional[UserResponse]: pass
