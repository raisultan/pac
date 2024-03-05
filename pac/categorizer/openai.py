import instructor
from openai import AsyncOpenAI as OpenAI
from pydantic import BaseModel, Field

from pac.categorizer.enums import TicketCategory
from pac.categorizer.interface import CategorizerClientInterface


class CategorizedTicket(BaseModel):
    category: TicketCategory = Field(
        description='Correctly assign one of the predefined categories to the ticket',
    )


class OpenAICategorizer(CategorizerClientInterface):
    def __init__(self, api_key: str):
        self._client = instructor.patch(OpenAI(api_key=api_key))

    async def run(self, text: str) -> TicketCategory:
        categorized = await self._client.chat.completions.create(
            model='gpt-3.5-turbo',
            response_model=CategorizedTicket,
            messages=[
                {'role': 'user', 'content': text},
            ]
        )
        return categorized.category
