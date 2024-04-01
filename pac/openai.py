import instructor
from openai import AsyncOpenAI as OpenAI
from pydantic import BaseModel, Field

from pac.enums import TicketCategory, TicketPriority
from pac.interface import PACLLMInterface


class PACTicket(BaseModel):
    priority: TicketPriority = Field(
        description='Correctly assign one of the predefined priorities to the support ticket',
    )
    category: TicketCategory = Field(
        description='Correctly assign one of the predefined categories to the support ticket',
    )


class OpenAIPACLLM(PACLLMInterface):
    def __init__(self, api_key: str):
        self._client = instructor.patch(OpenAI(api_key=api_key))

    async def run(self, text: str) -> TicketCategory:
        paced = await self._client.chat.completions.create(
            model='gpt-3.5-turbo',
            response_model=PACTicket,
            messages=[
                {'role': 'user', 'content': text},
            ]
        )
        return paced.priority, paced.category
