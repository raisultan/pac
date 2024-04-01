from typing import Final, Type, Optional

from pydantic import BaseModel

from pac.enums import TicketCategory, TicketPriority
from pac.interface import PACLLMInterface
from pac.normalizer import normalize
from pac.vectorizer import vectorize
from pac.vector_db.repository import TicketDTO, VectorDB


class Ticket(BaseModel):
    id: int
    email: str
    text: str


class TicketPACEvent(BaseModel):
    ticket: Ticket
    category: Optional[TicketCategory] = None
    priority: Optional[TicketPriority] = None
    is_llm_processed: bool = False


class PAC:
    SIMILARITY_THRESHOLD: Final[float] = 0.9

    def __init__(self, pac_llm_client: Type[PACLLMInterface], vector_db: VectorDB):
        self._pac_llm_client = pac_llm_client
        self._vector_db = vector_db

    async def categorize(self, ticket: Ticket) -> TicketPACEvent:
        event = TicketPACEvent(ticket=ticket)

        normalized_text = normalize(ticket.text)
        embedding = await vectorize(normalized_text)

        search_result = self._vector_db.search(embedding)
        filtered_results = [r for r in search_result if r['distance'] >= self.SIMILARITY_THRESHOLD]
        sorted_filtered_results = sorted(filtered_results, key=lambda r: r['distance'], reverse=True)

        print(f'Found {sorted_filtered_results} similar records.')

        if sorted_filtered_results:
            record = TicketDTO(
                id=ticket.id,
                email=ticket.email,
                text=normalized_text,
                priority=sorted_filtered_results[0]['priority'],
                category=sorted_filtered_results[0]['category'],
                embedding=embedding,
            )
            print(
                f'Found similar records with category {record.category}. '
                f'The most similar record {sorted_filtered_results[0]}'
                'Assigning the same category to the ticket.'
            )
        else:
            event.is_llm_processed = True
            priority, category = await self._pac_llm_client.run(normalized_text)
            if category == TicketCategory.OTHER:
                raise ValueError('Could not assign priority and category to the ticket')
            record = TicketDTO(
                id=ticket.id,
                email=ticket.email,
                text=normalized_text,
                priority=priority.value,
                category=category.value,
                embedding=embedding,
            )
            print(f'No similar tickets. Assigned category {record.priority} and {record.category} to the ticket.')

        event.category = record.category
        event.priority = record.priority
        self._vector_db.insert(record)
        return event
