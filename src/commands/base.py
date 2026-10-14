from abc import ABC, abstractmethod
from typing import Any




class AbstractCommand[_Return](ABC):

    @abstractmethod
    async def execute(self, *args, **kwargs) -> _Return: ...