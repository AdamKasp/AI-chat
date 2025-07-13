"""
OpenAI client service for AI model integration.
"""
from typing import List, Dict, Any, Optional
from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.API.Src.core.config import settings
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse


class OpenAIClient:
    """
    OpenAI client service for handling AI model interactions.
    """

    def __init__(self):
        """
        Initialize OpenAI client.
        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def completion(
        self,
        system_prompt: Optional[str],
        user_prompt: str,
        model: str = "gpt-4"
    ) -> AiResponse:
        """
        Create a chat completion using OpenAI API.

        Args:
            system_prompt: Optional system prompt to set context
            user_prompt: User's prompt/question
            model: Model to use for completion

        Returns:
            AiResponse: Mapped AI completion response

        Raises:
            Exception: If API call fails
        """
        try:
            # Build messages list
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt})

            chat_completion: ChatCompletion = self.client.chat.completions.create(
                messages=messages,
                model=model
            )

            # Map OpenAI response to AiResponse
            finish_reason = chat_completion.choices[0].finish_reason if chat_completion.choices else "unknown"
            answer = chat_completion.choices[0].message.content if chat_completion.choices and chat_completion.choices[0].message else ""
            
            # Extract relevant metadata
            metadata = {
                "usage": chat_completion.usage.model_dump() if chat_completion.usage else None
            }

            return AiResponse(finishReason=finish_reason, answer=answer, metadata=metadata)

        except Exception as error:
            print(f"Error in OpenAI completion: {error}")
            raise error
