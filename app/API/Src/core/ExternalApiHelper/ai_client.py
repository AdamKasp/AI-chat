from typing import Optional
from app.API.Src.core.ExternalApiHelper.OpenAI.openai_client import OpenAIClient
from app.API.Src.core.ExternalApiHelper.Gemini.gemini_client import GeminiClient
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse


async def completion(system_prompt: Optional[str], user_prompt: str, ai_model: str) -> AiResponse:
    if ai_model == "gpt-4":
        client = OpenAIClient()
        return await client.completion(system_prompt=system_prompt, user_prompt=user_prompt, model="gpt-4")
    elif ai_model in ["gemini-2.5-flash", "gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]:
        client = GeminiClient()
        return await client.completion(system_prompt=system_prompt, user_prompt=user_prompt, model=ai_model)
    else:
        raise ValueError(f"Unsupported AI model: {ai_model}")
