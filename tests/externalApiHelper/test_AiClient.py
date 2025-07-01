import pytest
from unittest.mock import AsyncMock, patch
from app.API.externalApiHelper.AiClient import completion
from app.API.externalApiHelper.model.AiResponse import AiResponse

@pytest.mark.asyncio
async def test_completion_calls_openai_client():
    mock_openai_client_instance = AsyncMock()
    mock_openai_client_instance.completion.return_value = AiResponse(
        finishReason="stop",
        answer="Test response from OpenAI",
        metadata={}
    )

    with patch('app.API.externalApiHelper.AiClient.OpenAIClient', return_value=mock_openai_client_instance) as MockOpenAIClient:
        messages = [{"role": "user", "content": "Hello"}]
        ai_tool = "OpenAI"
        
        response = await completion(messages=messages, ai_tool=ai_tool)
        
        MockOpenAIClient.assert_called_once()
        mock_openai_client_instance.completion.assert_called_once_with(messages=messages)
        assert isinstance(response, AiResponse)
        assert response.answer == "Test response from OpenAI"

@pytest.mark.asyncio
async def test_completion_unsupported_ai_tool():
    messages = [{"role": "user", "content": "Hello"}]
    ai_tool = "UnsupportedAI"
    
    with pytest.raises(ValueError, match="Unsupported AI tool: UnsupportedAI"):
        await completion(messages=messages, ai_tool=ai_tool)
