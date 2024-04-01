from abc import ABC, abstractmethod

from pac.enums import TicketCategory, TicketPriority


class PACLLMInterface(ABC):
    @abstractmethod
    async def run(self, text: str) -> tuple[TicketPriority, TicketCategory]: ...
