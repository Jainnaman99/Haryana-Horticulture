from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import get_session
from persistence.repositories.components.command.component_command_repository import ComponentCommandRepository
from application.services.components.command.component_command_service import ComponentCommandService


async def get_component_command_repository(
    session: AsyncSession = Depends(get_session),
) -> ComponentCommandRepository:
    return ComponentCommandRepository(session)


async def get_component_command_service(
    repo: ComponentCommandRepository = Depends(get_component_command_repository),
) -> ComponentCommandService:
    return ComponentCommandService(repo)
