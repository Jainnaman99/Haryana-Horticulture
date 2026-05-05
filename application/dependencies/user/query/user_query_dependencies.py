from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import get_session
from persistence.repositories.user.query.user_query_repository import UserQueryRepository
from application.services.user.query.user_query_service import UserQueryService


async def get_user_query_repository(
    session: AsyncSession = Depends(get_session),
) -> UserQueryRepository:
    return UserQueryRepository(session)

async def get_user_query_service(
    repo: UserQueryRepository = Depends(get_user_query_repository),
) -> UserQueryService:
    return UserQueryService(repo)

# def get_user_repository(session=Depends(get_session)):
#     return UserQueryRepository(session)


# def get_user_service(repo=Depends(get_session)):
#     return UserQueryService(repo)
