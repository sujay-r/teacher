from fastapi import APIRouter
from openai import OpenAI

from app.core.conversation import Conversation
from app.core.llm import OpenAILLM
from app.core.memory import ConversationMemory
from app.models.chat import Message

router = APIRouter(prefix='/api/chat')

openai_client = OpenAI()
gpt = OpenAILLM(openai_client)
conversation_memory = ConversationMemory()
conversation = Conversation(gpt, conversation_memory)


@router.post("/send_message")
async def send_message(message: Message):
    llm_reply = conversation.speak(message.message)
    return {"reply": llm_reply}
