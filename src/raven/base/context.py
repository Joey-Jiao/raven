from pathlib import Path
from typing import TypeVar

import punq

from .configs import ConfigTree, load_configs

T = TypeVar("T")


class ApplicationContext:
    def __init__(self, container: punq.Container):
        self._container = container

    def resolve(self, cls: type[T]) -> T:
        return self._container.resolve(cls)

    def register(self, *args, **kwargs):
        return self._container.register(*args, **kwargs)


def get_context(config_dir: str | Path = "configs") -> ApplicationContext:
    container = punq.Container()

    config = load_configs(config_dir)
    container.register(ConfigTree, instance=config)

    return ApplicationContext(container)
