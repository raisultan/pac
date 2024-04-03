from typing import Optional, Protocol

from pac.enums import TicketCategory, TicketPriority
from pac.vector_db.repository import TicketDTO, VectorDB


class HasPriorityAndCategory(Protocol):
    priority: TicketPriority
    category: TicketCategory


class Updater:
    def __init__(self, vector_db: VectorDB):
        self._vector_db = vector_db

    def run(self, id: int, pac: HasPriorityAndCategory) -> Optional[TicketDTO]:
        ticket = self._vector_db.get(id)
        if not ticket: return None

        updated_ticket = TicketDTO(
            id=ticket.id,
            email=ticket.email,
            text=ticket.text,
            priority=pac.priority.value,
            category=pac.category.value,
            embedding=ticket.embedding,
        )
        self._vector_db.update(updated_ticket)
        return updated_ticket
