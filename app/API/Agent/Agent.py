from fastapi import APIRouter
from typing import Dict, List
from app.API.externalApiHelper.AiClient import completion
from app.API.externalApiHelper.model.AiResponse import AiResponse

router = APIRouter()

@router.post("/chat", response_model=AiResponse)
async def chat(prompt: str, model: str):
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": prompt}
    ]
    response: AiResponse = await completion(messages=messages, ai_tool="OpenAI")
    return response