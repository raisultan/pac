import os

from dotenv import load_dotenv

from pac.categorizer.openai import OpenAICategorizer
from pac.vector_db.repository import VectorDB
from pac.vector_db.milvus import MilvusRepository
from pac.categorizer.categorizer import Categorizer

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')

vector_db = VectorDB(MilvusRepository())
categorizer_client = OpenAICategorizer(api_key)
categorizer = Categorizer(categorizer_client, vector_db)
