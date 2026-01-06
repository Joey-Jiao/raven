from pathlib import Path

import punq

from .configs import ConfigService


class ApplicationContext:
    def __init__(self, container: punq.Container):
        self._container = container

    def resolve(self, cls):
        return self._container.resolve(cls)

    def register(self, *args, **kwargs):
        return self._container.register(*args, **kwargs)


def get_context(
        config_dir: str = "configs",
        env_path: str = ".env",
) -> ApplicationContext:
    container = punq.Container()

    config_files = list(Path(config_dir).glob("*.yaml"))
    config_service = ConfigService(config_dir=config_files, env_path=env_path)
    container.register(ConfigService, instance=config_service)

    return ApplicationContext(container)
