from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.API.Src.Chat.repository.chat_repository import ChatRepository
from app.API.Src.Chat.repository.message_repository import MessageRepository


class DeleteChatController:
    @staticmethod
    async def delete_chat(chat_id: UUID, db: AsyncSession):
        chat_repository = ChatRepository(db)
        message_repository = MessageRepository(db)
        
        # Check if chat exists
        chat = await chat_repository.get_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Delete all messages associated with the chat
        await message_repository.delete_by_chat_id(chat_id)
        
        # Delete the chat
        await chat_repository.delete(chat_id)
        
        return {"message": "Chat and associated messages deleted successfully"}