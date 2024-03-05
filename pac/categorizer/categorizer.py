from typing import Final, Type

from pydantic import BaseModel

from pac.categorizer.enums import TicketCategory
from pac.categorizer.interface import CategorizerClientInterface
from pac.normalizer import normalize
from pac.vectorizer import vectorize
from pac.vector_db.repository import TicketDTO, VectorDB


class Ticket(BaseModel):
    id: int
    email: str
    text: str


class Categorizer:
    SIMILARITY_THRESHOLD: Final[float] = 0.9

    def __init__(self, categorizer_client: Type[CategorizerClientInterface], vector_db: VectorDB):
        self._categorizer_client = categorizer_client
        self._vector_db = vector_db

    async def categorize(self, ticket: Ticket) -> None:
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
                category=sorted_filtered_results[0]['category'],
                embedding=embedding,
            )
            print(
                f'Found similar records with category {record.category}. '
                f'The most similar record {sorted_filtered_results[0]}'
                'Assigning the same category to the ticket.'
            )
        else:
            category = await self._categorizer_client.run(normalized_text)
            if category == TicketCategory.OTHER:
                raise ValueError('Could not categorize the ticket')
            record = TicketDTO(
                id=ticket.id,
                email=ticket.email,
                text=normalized_text,
                category=category.name,
                embedding=embedding,
            )
            print(f'No similar tickets. Assigned category {record.category} to the ticket.')

        self._vector_db.insert(record)
