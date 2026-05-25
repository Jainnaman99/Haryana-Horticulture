from sqlalchemy.ext.asyncio import AsyncSession
from domain.interfaces.components.command.icomponent_command_repository import IComponentCommandRepository


class ComponentCommandRepository(IComponentCommandRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
