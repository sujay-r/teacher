from fastapi import APIRouter
from app.models.chat import Message
from app.core.llm import get_llm_response

router = APIRouter(prefix='/api/chat')


@router.post("/send_message")
async def send_message(message: Message):
    llm_reply = get_llm_response(message.message)
    return {"reply": llm_reply}
