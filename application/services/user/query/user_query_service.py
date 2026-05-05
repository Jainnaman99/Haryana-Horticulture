from typing import List
# from persistence.repositories.user.query.user_query_repository import UserQueryRepository
from domain.interfaces.user.query.iuser_query_repository import IUserQueryRepository
from application.services.user.dto.user_dto import UserDTO
from uuid import UUID
class UserQueryService:
    def __init__(self, user_query_repository: IUserQueryRepository):
        self.user_query_repository = user_query_repository

    # async def get_all_users(self) -> List[UserDTO]:
    #     return await self.user_query_repository.get_all_users()
    
    async def get_all_users(self):
        return await self.user_query_repository.get_all_users()

    async def get_user_by_id(self, user_id: int):
        return await self.user_query_repository.get_user_by_id(user_id)
