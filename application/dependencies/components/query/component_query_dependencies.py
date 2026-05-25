from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import get_session
from persistence.repositories.components.query.component_query_repository import ComponentQueryRepository
from application.services.components.query.component_query_service import ComponentQueryService


async def get_component_query_repository(
    session: AsyncSession = Depends(get_session),
) -> ComponentQueryRepository:
    return ComponentQueryRepository(session)


async def get_component_query_service(
    repo: ComponentQueryRepository = Depends(get_component_query_repository),
) -> ComponentQueryService:
    return ComponentQueryService(repo)
