from abc import ABC, abstractmethod
from typing import List, Dict

from app.models.chat import ConversationTurn, Message


class MessageFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_message() -> Message:
        pass

    @staticmethod
    @abstractmethod
    def create_message_array() -> List[Message]:
        pass


class SimpleMessageFactory(MessageFactory):
    @staticmethod
    def create_message(content: str) -> Message:
        return Message(content=content)
    
    @staticmethod
    def create_message_array(content_list: List[str]) -> List[Message]:
        return [SimpleMessageFactory.create_message(content) for content in content_list]


class ConversationTurnFactory(MessageFactory):
    @staticmethod
    def create_message(content: str, role: str) -> ConversationTurn:
        return ConversationTurn(content=content, role=role)

    @staticmethod
    def create_message_array(messages: List[Dict[str, str]]) -> List[ConversationTurn]:
        return [ConversationTurnFactory.create_message(**item) for item in messages]
