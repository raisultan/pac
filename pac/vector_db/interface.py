from abc import ABC, abstractmethod


class VectorDBInterface(ABC):
    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def disconnect(self) -> None: ...

    @abstractmethod
    def insert(self, records: list[dict]) -> None: ...

    @abstractmethod
    def update(self, records: list[dict]) -> None: ...

    @abstractmethod
    def search(self, embedding: list[float], topK: int) -> list[dict]: ...

    @abstractmethod
    def delete_by_ids(self, ids: list[int]) -> None: ...
