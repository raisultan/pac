from pydantic import BaseModel

from pac.categorizer import categorize, TicketCategory
from pac.normalizer import normalize
from pac.vectorizer import vectorize
from pac.vector_db.repository import TicketDTO, VectorDB
from pac.vector_db.milvus import MilvusRepository


class Ticket(BaseModel):
    id: int
    email: str
    text: str


SIMILARITY_THRESHOLD = 0.9


async def process(ticket: Ticket) -> None:
    normalized_text = normalize(ticket.text)
    embedding = await vectorize(normalized_text)

    vector_db = VectorDB(MilvusRepository())
    vector_db.connect()

    search_result = vector_db.search(embedding)
    filtered_results = [r for r in search_result if r['distance'] >= SIMILARITY_THRESHOLD]
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
        category = await categorize(normalized_text)
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

    vector_db.insert(record)
    vector_db.disconnect()
