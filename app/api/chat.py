from openai import OpenAI
from fastapi import APIRouter

from app.models.chat import Message
from app.core.llm import get_llm_response
from app.core.llm import OpenAILLM
from app.core.memory import ConversationMemory
from app.core.conversation import Conversation

router = APIRouter(prefix='/api/chat')

openai_client = OpenAI()
gpt = OpenAILLM(openai_client)
conversation_memory = ConversationMemory()
conversation = Conversation(gpt, conversation_memory)


@router.post("/send_message")
async def send_message(message: Message):
    llm_reply = conversation.speak(message.message)
    return {"reply": llm_reply}
