from pac.vector_db.milvus import MilvusRepository


class VectorDB:
    def __init__(self, repository: MilvusRepository):
        self.repository = repository
