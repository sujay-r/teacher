from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from app.models.chat import ConversationTurn
from app.models.enums import Speaker


class Memory(ABC):
    @abstractmethod
    def add_object_to_memory(self, object: Dict[str, str]) -> None:
        '''Adds given object to memory'''


def default_conversation_history() -> list:
    return []

class ConversationMemory(Memory):
    def __init__(self, existing_history: Optional[List[ConversationTurn]]=None) -> None:
        self.conversation_history = []
        if existing_history:  # Can't use a blank list as default because it causes memory leaks.
            self.conversation_history = existing_history

    @staticmethod
    def initialise_from_existing_conversation_history(conversation_history: List[Dict[str, str]]) -> 'ConversationMemory':
        processed_history = ConversationMemory.normalize_raw_conversation_history(conversation_history)
        return ConversationMemory(existing_history=processed_history)

    @staticmethod
    def normalize_raw_conversation_history(conversation_history: List[Dict[str, str]]) -> List[ConversationTurn]:
        return [ConversationTurn(**item) for item in conversation_history]

    def get_conversation_history_for_llm_call(self) -> List[Dict[str, str]]:
        return ConversationMemory.denormalize_conversation_history(
            self.conversation_history
        )

    @staticmethod
    def denormalize_conversation_history(conversation_history: List[ConversationTurn]) -> List[Dict[str, str]]:
        return [item.model_dump(by_alias=True) for item in conversation_history]

    def add_object_to_memory(self, object: ConversationTurn) -> None:
        self.conversation_history.append(object)

    # TODO: Address the code duplication between the add_user_message and add_llm_message methods.
    def add_user_message_to_memory(self, user_message: str) -> None:
        user_turn = self.create_user_turn_from_message(user_message)
        self.add_object_to_memory(user_turn)

    def add_llm_message_to_memory(self, llm_message: str) -> None:
        llm_turn = self.create_llm_turn_from_message(llm_message)
        self.add_object_to_memory(llm_turn)    

    # TODO: Abstract this responsibility to a data factory class
    def create_user_turn_from_message(self, user_message: str) -> ConversationTurn:
        return ConversationTurn(role=Speaker.HUMAN.value, content=user_message)

    # TODO: Abstract this responsibility to a data factory class
    def create_llm_turn_from_message(self, llm_response: str) -> ConversationTurn:
        return ConversationTurn(role=Speaker.AGENT.value, content=llm_response)
