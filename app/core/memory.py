from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app.models import ConversationTurnFactory
from app.models.chat import ConversationTurn
from app.models.enums import Speaker


class Memory(ABC):
    @abstractmethod
    def add_object_to_memory(self, object: Dict[str, str]) -> None:
        '''Adds given object to memory'''


class ConversationMemory(Memory):
    def __init__(self, existing_history: Optional[List[ConversationTurn]]=None) -> None:
        self.conversation_history = []
        if existing_history:  # Can't use a blank list as default because it causes memory leaks.
            self.conversation_history = existing_history

    @staticmethod
    def initialise_from_existing_conversation_history(conversation_history: List[Dict[str, str]]) -> 'ConversationMemory':
        processed_history = ConversationTurnFactory.create_message_array(conversation_history)
        return ConversationMemory(existing_history=processed_history)

    def get_conversation_history_for_llm_call(self) -> List[Dict[str, str]]:
        return ConversationMemory.denormalize_conversation_history(
            self.conversation_history
        )

    # TODO: Look into how cohesive this method really is to this class.
    @staticmethod
    def denormalize_conversation_history(conversation_history: List[ConversationTurn]) -> List[Dict[str, str]]:
        return [item.model_dump(by_alias=True) for item in conversation_history]
    
    # TODO: Think about whether this abstraction even makes sense
    # (Since it's a wrapper around the abstract interface itself)
    # (Look into whether the abstract interface needs to be redesigned properly or not)
    def add_user_message_to_memory(self, user_message: str) -> None:
        self.add_message_to_memory(user_message, Speaker.HUMAN.value)

    def add_llm_message_to_memory(self, llm_message: str) -> None:
        self.add_message_to_memory(llm_message, Speaker.AGENT.value)

    def add_message_to_memory(self, message, speaker):
        conversation_turn = ConversationTurnFactory.create_message(
            content=message, role=speaker
        )
        self.add_object_to_memory(conversation_turn)

    def add_object_to_memory(self, object: ConversationTurn) -> None:
        self.conversation_history.append(object)
