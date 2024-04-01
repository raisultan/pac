import os

from dotenv import load_dotenv
from faststream import FastStream
from faststream.kafka import KafkaBroker

from pac.openai import OpenAIPACLLM
from pac.vector_db.repository import VectorDB
from pac.vector_db.milvus import MilvusRepository
from pac.pac import PAC, Ticket

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
vector_db = VectorDB(MilvusRepository())
pac_llm_client = OpenAIPACLLM(api_key)
pac = PAC(pac_llm_client, vector_db)

broker = KafkaBroker('localhost:29092')
app = FastStream(broker)


@app.on_startup
async def setup_vector_db():
    vector_db.connect()


@app.on_shutdown
async def shutdown_vector_db():
    vector_db.disconnect()


@broker.subscriber('test')
@broker.publisher('test_out')
async def handle_ticket(ticket: Ticket):
    print(f'Handling ticket: {ticket}')
    event = await pac.categorize(ticket)
    return event
