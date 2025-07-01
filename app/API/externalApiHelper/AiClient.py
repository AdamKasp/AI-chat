from typing import List, Dict
from app.API.externalApiHelper.OpenAI.OpenAIClient import OpenAIClient
from app.API.externalApiHelper.model.AiResponse import AiResponse


async def completion(messages: List[Dict[str, str]], ai_tool: str) -> AiResponse:
    if ai_tool == "gpt-4":
        client = OpenAIClient()
        return await client.completion(messages=messages, model="gpt-4")
    else:
        raise ValueError(f"Unsupported AI tool: {ai_tool}")
