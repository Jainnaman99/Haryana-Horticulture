from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.entities.user import User
from datetime import datetime
from application.services.user.dto.user_dto import UserCreate, UserResponse, UserUpdate
from domain.interfaces.user.command.iuser_command_repository import IUserCommandRepository

class UserCommandRepository(IUserCommandRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            db_user = await self.db.get(User, user.UserId)
            return UserResponse.model_validate(db_user)  # ORM -> Pydantic
        except Exception as e:
            await self.db.rollback()
            raise e  # re-raise to propagate error

    async def update_user(self, user_id: UUID, request: UserUpdate) -> UserResponse | None:
        try:
            result = await self.db.execute(select(User).where(User.UserId == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return None

            # Convert Pydantic -> dict for update
            update_data = request.model_dump(exclude_unset=True)
            update_data["ModifiedOn"] = datetime.utcnow()  # update timestamp

            for key, value in update_data.items():
                setattr(user, key, value)

            await self.db.commit()
            await self.db.refresh(user)
            db_user = await self.db.get(User, user.UserId)
            return UserResponse.model_validate(db_user)
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_user(self, user_id: UUID) -> User | None:
        try:
            result = await self.db.execute(select(User).where(User.UserId == user_id))
            user = result.scalar_one_or_none()

            if not user:
                return None

            await self.db.delete(user)
            await self.db.commit()
            return user
        except Exception as e:
            await self.db.rollback()
            raise e
