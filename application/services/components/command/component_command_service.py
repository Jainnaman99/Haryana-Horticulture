from domain.interfaces.components.command.icomponent_command_repository import IComponentCommandRepository


class ComponentCommandService:
    def __init__(self, repo: IComponentCommandRepository):
        self.repo = repo
