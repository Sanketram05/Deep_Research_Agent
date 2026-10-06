from agents import Agent, function_tool
from agents.model_settings import ModelSettings
from dotenv import load_dotenv

import os
import requests

load_dotenv(override=True)

from models import GEMINI_MODEL

@function_tool
def web_search(query: str) -> str:
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": os.getenv("TAVILY_API_KEY"),
            "query": query,
            "max_results": 3
        }
    )

    data = response.json()

    results = []

    for result in data.get("results", []):
        results.append(
            f"Title: {result.get('title')}\n"
            f"URL: {result.get('url')}\n"
            f"Content: {result.get('content')}"
        )

    return "\n\n".join(results)

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

settings = ModelSettings(tool_choice="required")
tools = [web_search]

search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, tools=tools, model=GEMINI_MODEL, model_settings=settings)