from abc import ABC, abstractmethod
from typing import Dict
from openai import OpenAI

client = OpenAI()

chat_history = []


class LLM(ABC):
    @abstractmethod
    def call_llm(self, messages: Dict[str, str]) -> None:
        '''Sends a message to the LLM'''


class OpenAILLM(LLM):
    def __init__(self, openai_client: OpenAI) -> None:
        self.openai_client = openai_client
    
    def call_llm(self, messages: Dict[str, str]) -> None:
        pass


def get_llm_response(user_message: str) -> str:
    user_message_object = create_message_object(role='user', message=user_message)
    chat_history.append(user_message_object)

    openai_response_object = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=chat_history,
    )
    llm_response = openai_response_object.choices[0].message.content
    llm_response_object = create_message_object(role='assistant', message=llm_response)
    chat_history.append(llm_response_object)

    return llm_response


def create_message_object(role: str, message: str) -> Dict[str, str]:
    return {
        'role': role,
        'content': message
    }