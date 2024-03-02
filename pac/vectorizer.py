import os

from openai import AsyncOpenAI as OpenAI
from dotenv import load_dotenv

EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'


load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


async def vectorize(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    response = await client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
