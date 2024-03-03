import os
from enum import Enum, auto

import instructor
from dotenv import load_dotenv
from openai import AsyncOpenAI as OpenAI
from pydantic import BaseModel, Field

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
client = instructor.patch(OpenAI(api_key=api_key))


class TicketCategory(Enum):
    ACCOUNT_ACCESS = auto()
    BATTERY_LIFE = auto()
    CANCELLATION_REQUEST = auto()
    DATA_LOSS = auto()
    DELIVERY_PROBLEM = auto()
    DISPLAY_ISSUE = auto()
    HARDWARE_ISSUE = auto()
    INSTALLATION_SUPPORT = auto()
    NETWORK_PROBLEM = auto()
    PAYMENT_ISSUE = auto()
    PERIPHERAL_COMPATIBILITY = auto()
    PRODUCT_COMPATIBILITY = auto()
    PRODUCT_RECOMMENDATION = auto()
    PRODUCT_SETUP = auto()
    REFUND_REQUEST = auto()
    SOFTWARE_BUG = auto()
    OTHER = auto()


class CategorizedTicket(BaseModel):
    category: TicketCategory = Field(description='Correctly assign one of the predefined categories to the ticket')


async def categorize(text: str) -> CategorizedTicket:
    categorized = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        response_model=CategorizedTicket,
        messages=[
            {'role': 'user', 'content': text},
        ]
    )
    return categorized
