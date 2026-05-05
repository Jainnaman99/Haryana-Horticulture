from abc import ABC, abstractmethod
from typing import List,Optional
from application.services.user.dto.user_dto import UserDTO
from uuid import UUID
from domain.entities.user import User


class IUserQueryRepository(ABC):
    # @abstractmethod
    # async def get_all_users(self) -> List[UserDTO]:
    #     """Fetch all users"""
    #     pass

    @abstractmethod
    async def get_all_users(self) -> List[User]: pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]: pass

