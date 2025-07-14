import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.API.Src.Chat.controller.delete_chat import DeleteChatController
from app.API.Src.Chat.models.chat_history import ChatHistory


@pytest.mark.asyncio
async def test_delete_chat_success():
    # Arrange
    chat_id = uuid4()
    mock_db = AsyncMock()
    
    # Mock chat exists
    mock_chat = MagicMock(spec=ChatHistory)
    mock_chat.id = chat_id
    
    # Mock repositories
    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_by_id.return_value = mock_chat
    mock_chat_repo.delete.return_value = None
    
    mock_message_repo = AsyncMock()
    mock_message_repo.delete_by_chat_id.return_value = None
    
    # Mock repository creation
    with pytest.mock.patch('app.API.Src.Chat.controller.delete_chat.ChatRepository', return_value=mock_chat_repo):
        with pytest.mock.patch('app.API.Src.Chat.controller.delete_chat.MessageRepository', return_value=mock_message_repo):
            # Act
            result = await DeleteChatController.delete_chat(chat_id, mock_db)
            
            # Assert
            assert result == {"message": "Chat and associated messages deleted successfully"}
            mock_chat_repo.get_by_id.assert_called_once_with(chat_id)
            mock_message_repo.delete_by_chat_id.assert_called_once_with(chat_id)
            mock_chat_repo.delete.assert_called_once_with(chat_id)


@pytest.mark.asyncio
async def test_delete_chat_not_found():
    # Arrange
    chat_id = uuid4()
    mock_db = AsyncMock()
    
    # Mock chat doesn't exist
    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_by_id.return_value = None
    
    mock_message_repo = AsyncMock()
    
    # Mock repository creation
    with pytest.mock.patch('app.API.Src.Chat.controller.delete_chat.ChatRepository', return_value=mock_chat_repo):
        with pytest.mock.patch('app.API.Src.Chat.controller.delete_chat.MessageRepository', return_value=mock_message_repo):
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await DeleteChatController.delete_chat(chat_id, mock_db)
            
            assert exc_info.value.status_code == 404
            assert exc_info.value.detail == "Chat not found"
            mock_chat_repo.get_by_id.assert_called_once_with(chat_id)
            mock_message_repo.delete_by_chat_id.assert_not_called()
            mock_chat_repo.delete.assert_not_called()