from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from dotenv import load_dotenv

import os

load_dotenv(override=True)

mixroute_client = AsyncOpenAI(
    api_key=os.getenv("MIXROUTE_API_KEY"),
    base_url="https://api.mixroute.ai/v1"
)

GEMINI_MODEL = OpenAIChatCompletionsModel(
    model="gemini-3.5-flash-lite",
    openai_client=mixroute_client
)

DEEPSEEK_MODEL = OpenAIChatCompletionsModel(
    model="deepseek-v4-flash",
    openai_client=mixroute_client
)