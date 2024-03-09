import os

from dotenv import load_dotenv
from faststream import FastStream
from faststream.kafka import KafkaBroker

from pac.categorizer.openai import OpenAICategorizer
from pac.vector_db.repository import VectorDB
from pac.vector_db.milvus import MilvusRepository
from pac.categorizer.categorizer import Categorizer, Ticket

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
broker = KafkaBroker('localhost:29092')

app = FastStream(broker)
vector_db = VectorDB(MilvusRepository())
categorizer_client = OpenAICategorizer(api_key)
categorizer = Categorizer(categorizer_client, vector_db)

@app.on_startup
async def setup_vector_db():
    vector_db.connect()

@app.on_shutdown
async def shutdown_vector_db():
    vector_db.disconnect()


@broker.subscriber('test')
async def handle_ticket(ticket: Ticket):
    print(f'Handling ticket: {ticket}')
    await categorizer.categorize(ticket)