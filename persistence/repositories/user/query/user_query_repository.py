from typing import List,Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from application.services.user.dto.user_dto import UserDTO
from domain.entities.user import User
from uuid import UUID
from sqlalchemy import select, update, delete
from domain.interfaces.user.query.iuser_query_repository import IUserQueryRepository

class UserQueryRepository(IUserQueryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def get_all_users(self) -> List[UserDTO]:
    #     # query = text("EXEC Usp_GetUsers")
    #     query = text("Select * from Users")
    #     result = await self.session.execute(query)
    #     rows = result.fetchall()

    #     return [UserDTO(**row._mapping) for row in rows]
    
    
    async def get_all_users(self):
        stmt = text("EXEC ProcGetAllUsers")   # or your proc name
        result = await self.session.execute(stmt)
        return result.mappings().all()

    # async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
    #     """Get user by ID"""
    #     stmt = select(User).where(User.UserId == user_id)
    #     result = await self.session.execute(stmt)
    #     return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> Optional[dict]:
        stmt = text("EXEC GetUserById :user_id")

        result = await self.session.execute(
            stmt,
            {"user_id": str(user_id)}  # pass as string for SQL Server
        )

        row = result.mappings().first()
        return row if row else None

