from dataclasses import dataclass

from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections

from pac.vector_db.interface import VectorDBInterface


@dataclass(frozen=True)
class MilvusCollectionConfig:
    index_type: str
    metric_type: str
    params: dict


class MilvusRepository(VectorDBInterface):

    VECTOR_DIMENSIONS = 1536

    id_field = FieldSchema(name='id', dtype=DataType.INT64, is_primary=True)
    email_field = FieldSchema(name='email', dtype=DataType.VARCHAR, max_length=256)
    text_field = FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=512)
    priority_field = FieldSchema(name='priority', dtype=DataType.VARCHAR, max_length=256)
    category_field = FieldSchema(name='category', dtype=DataType.VARCHAR, max_length=256)
    embedding_field = FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIMENSIONS)
    schema = CollectionSchema(
        fields=[id_field, email_field, text_field, priority_field, category_field, embedding_field],
        description='Support Tickets Collection',
    )
    collection_name = 'tickets'

    index_config = MilvusCollectionConfig(
        index_type='HNSW',
        metric_type='COSINE',
        params={'M': 24, 'efConstruction': 256},
    )

    def __init__(
        self,
        alias: str = 'default',
        user: str = 'username',
        password: str = 'password',
        host: str = 'localhost',
        port: str = '19530',
    ):
        self._alias = alias
        self._user = user
        self._password = password
        self._host = host
        self._port = port

    def connect(self):
        connections.connect(
            alias=self._alias,
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
        )

    def disconnect(self) -> None:
        connections.disconnect(self._alias)

    def create_collection(self) -> Collection:
        collection = Collection(
            name=self.collection_name,
            schema=self.schema,
        )
        self._build_indexes()
        return collection

    def get_collection(self) -> Collection:
        return Collection(name=self.collection_name)

    def insert(self, records: list[dict]) -> None:
        collection = self.get_collection()
        collection.load()
        collection.insert(records)
        collection.flush()

    def update(self, records: list[dict]) -> None:
        collection = self.get_collection()
        collection.load()
        collection.upsert(records)
        collection.flush()

    def search(self, embedding: list[float], topK: int) -> list[dict]:
        collection = self.get_collection()
        collection.load()
        search_params = {'metric_type': self.index_config.metric_type, 'params': self.index_config.params}
        raw_result = collection.search(
            [embedding],
            'embedding',
            search_params,
            limit=topK,
            output_fields=['id', 'priority', 'category', 'text'],
        )
        result = []
        for hits in raw_result:
            for hit in hits:
                entity = hit.entity
                result.append({
                    'id': entity.get('id'),
                    'priority': entity.get('priority'),
                    'category': entity.get('category'),
                    'text': entity.get('text'),
                    'distance': hit.distance,
                })
        return result

    def delete_by_ids(self, ids: list[int]) -> None:
        collection = self.get_collection()
        collection.load()
        expr = f'id in [{", ".join(map(str, ids))}]'
        collection.delete(expr)
        collection.flush()

    def _build_indexes(self) -> None:
        collection = self.get_collection()
        index = {
            'index_type': self.index_config.index_type,
            'metric_type': self.index_config.metric_type,
            'params': self.index_config.params,
        }
        collection.create_index(field_name='embedding', index_params=index)
