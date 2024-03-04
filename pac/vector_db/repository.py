from dataclasses import dataclass

from pac.vector_db.milvus import MilvusRepository


@dataclass(frozen=True)
class TicketDTO:
    id: int
    email: str
    text: str
    category: str
    embedding: list

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'text': self.text,
            'category': self.category,
            'embedding': self.embedding,
        }


class VectorDB:
    def __init__(self, repository: MilvusRepository):
        self.repository = repository

    def connect(self):
        self.repository.connect()

    def disconnect(self):
        self.repository.disconnect()

    def search(self, embedding: list[float], top_k: int = 5) -> list:
        return self.repository.search(embedding, top_k)

    def insert(self, record: TicketDTO) -> None:
        self.repository.insert([record.to_dict()])

    def update(self, record: TicketDTO) -> None:
        self.repository.update([record.to_dict()])

    def delete(self, record: TicketDTO) -> None:
        self.repository.delete_by_ids([record.id])
