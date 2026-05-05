from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import get_session
from persistence.repositories.user.command.user_command_repository import UserCommandRepository
from application.services.user.command.user_command_service import UserCommandService


async def get_user_command_repository(
    session: AsyncSession = Depends(get_session),
) -> UserCommandRepository:
    return UserCommandRepository(session)

async def get_user_command_service(
    repo: UserCommandRepository = Depends(get_user_command_repository),
) -> UserCommandService:
    return UserCommandService(repo)