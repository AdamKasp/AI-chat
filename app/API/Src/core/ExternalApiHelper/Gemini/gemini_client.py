"""
Gemini client service for AI model integration.
"""
from typing import List, Dict, Any, Optional
import google.generativeai as genai

from app.API.Src.core.config import settings
from app.API.Src.core.ExternalApiHelper.model.ai_response import AiResponse


class GeminiClient:
    """
    Gemini client service for handling Google AI model interactions.
    """

    def __init__(self):
        """
        Initialize Gemini client.
        """
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
    async def completion(
        self,
        system_prompt: Optional[str],
        user_prompt: str,
        model: str = "gemini-2.5-flash"
    ) -> AiResponse:
        """
        Create a chat completion using Gemini API.

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
            # Initialize the model with system instructions if provided
            if system_prompt:
                # Gemini handles system prompts differently - they're passed as system_instruction
                gemini_model = genai.GenerativeModel(
                    model_name=model,
                    system_instruction=system_prompt
                )
            else:
                gemini_model = genai.GenerativeModel(model)
            
            # Generate content with user prompt
            response = gemini_model.generate_content(user_prompt)
            
            # Map Gemini response to AiResponse
            # Gemini doesn't provide finish_reason in the same way as OpenAI
            finish_reason = "stop"  # Default to "stop" for successful completions
            answer = response.text if response.text else ""
            
            # Extract metadata
            metadata = {
                "model": model,
                "prompt_tokens": None,  # Gemini API doesn't provide token counts in the same way
                "completion_tokens": None,
                "total_tokens": None
            }
            
            # Add safety ratings if available
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'safety_ratings'):
                    metadata["safety_ratings"] = [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        }
                        for rating in candidate.safety_ratings
                    ]
                if hasattr(candidate, 'finish_reason'):
                    finish_reason = candidate.finish_reason.name.lower()

            return AiResponse(finishReason=finish_reason, answer=answer, metadata=metadata)

        except Exception as error:
            print(f"Error in Gemini completion: {error}")
            raise error