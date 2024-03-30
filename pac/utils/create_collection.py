from pac.vector_db.milvus import MilvusRepository

milvus = MilvusRepository()
milvus.connect()
milvus.create_collection()
print('Collection created successfully.')
milvus.disconnect()
