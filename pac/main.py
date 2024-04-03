import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from faststream.kafka.fastapi import KafkaRouter

from pac.openai import OpenAIPACLLM
from pac.vector_db.repository import VectorDB
from pac.vector_db.milvus import MilvusRepository
from pac.pac import PAC, Ticket
from pac.updater import Updater
from pac.schemas import TicketResponse, UpdateTicketRequest

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
vector_db = VectorDB(MilvusRepository())
updater = Updater(vector_db)
pac_llm_client = OpenAIPACLLM(api_key)
pac = PAC(pac_llm_client, vector_db)

router = KafkaRouter("localhost:29092")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with (router.lifespan_context(app)):
        vector_db.connect()
        yield
        vector_db.disconnect()


@router.subscriber('tickets')
@router.publisher('processed_tickets')
async def handle_ticket(ticket: Ticket):
    event = await pac.categorize(ticket)
    return event


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get('/api/tickets/{id}')
def get_ticket_handler(id: int) -> TicketResponse:
    ticket = vector_db.get(id)
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    result = TicketResponse(
        id=ticket.id,
        text=ticket.text,
        priority=ticket.priority,
        category=ticket.category,
    )
    return result


@app.patch('/api/tickets/{id}')
async def update_ticket_handler(
    id: int,
    req: UpdateTicketRequest,
) -> TicketResponse:
    updated_ticket = updater.run(id, req)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')

    response = TicketResponse(
        id=updated_ticket.id,
        text=updated_ticket.text,
        priority=updated_ticket.priority,
        category=updated_ticket.category,
    )

    await router.broker.publish(response.model_dump_json(), 'corrected_tickets')
    return response
