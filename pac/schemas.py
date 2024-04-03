from pydantic import BaseModel

from pac.enums import TicketCategory, TicketPriority


class UpdateTicketRequest(BaseModel):
    priority: TicketPriority
    category: TicketCategory


class TicketResponse(BaseModel):
    id: int
    text: str
    priority: str
    category: str
