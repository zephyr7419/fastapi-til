from dependency_injector import containers, providers

from user.application.user_service import UserService
from user.infra.repository.user_repo import UserStore


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user.interface.controllers"],
    )

    user_repo = providers.Factory(UserStore)
    user_service = providers.Factory(UserService, user_repo = user_repo)
