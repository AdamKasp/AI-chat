def get_prompts(context: str, prompt: str) -> tuple[str, str]:
    if context.strip():
        system_prompt = f"""You are a helpful AI assistant. Answer user questions based on the provided context from documents and conversation history with the user (in CHAT HISTORY, you have the conversation with the user, respond based on that as well).

DOCUMENT CONTEXT:
{context}

Rules:
1. Use information from the above context to answer
2. Also use information from chat history (CHAT HISTORY section) - this contains previous interactions between the user and the model
3. if those two sources are not enough, use your own knowledge to answer the question but tell the user that you are using your own knowledge
4. If the user asks about information they previously shared in the conversation - recorded in CHAT HISTORY - use information from the history
5. Answer in language of the user
"""
        
        user_prompt = f"Based on the provided context, answer the question: {prompt}"
    else:
        system_prompt = "End each response with the sentence 'I HOPE THIS HELPED'"
        user_prompt = f"Answer the user's question: {prompt}"
    
    return system_prompt, user_prompt