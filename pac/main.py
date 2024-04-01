import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from faststream.kafka.fastapi import KafkaRouter

from pac.openai import OpenAIPACLLM
from pac.vector_db.repository import VectorDB
from pac.vector_db.milvus import MilvusRepository
from pac.pac import PAC, Ticket

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
vector_db = VectorDB(MilvusRepository())
pac_llm_client = OpenAIPACLLM(api_key)
pac = PAC(pac_llm_client, vector_db)

router = KafkaRouter("localhost:29092")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with (router.lifespan_context(app)):
        vector_db.connect()
        yield
        vector_db.disconnect()


@router.subscriber('test')
@router.publisher('test_out')
async def handle_ticket(ticket: Ticket):
    print(f'Handling ticket: {ticket}')
    event = await pac.categorize(ticket)
    return event


app = FastAPI(lifespan=lifespan)
app.include_router(router)
