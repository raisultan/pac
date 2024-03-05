from abc import ABC, abstractmethod

from pac.categorizer.enums import TicketCategory


class CategorizerClientInterface(ABC):
    @abstractmethod
    async def run(self, text: str) -> TicketCategory: ...
