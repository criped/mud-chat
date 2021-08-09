from abc import ABC, abstractmethod


class LookElementAbstract(ABC):
    TEMPLATE: str

    @abstractmethod
    def __init__(self, connection, *args, **kwargs):
        ...

    @abstractmethod
    async def get_element_str(self) -> str:
        ...
