from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from app.models.chat import ConversationTurn
from app.models.enums import Speaker


class Memory(ABC):
    @abstractmethod
    def add_object_to_memory(self, object: Dict[str, str]) -> None:
        '''Adds given object to memory'''


class ConversationMemory(Memory):
    def __init__(self, existing_history: Optional[List[Dict[str, str]]]) -> None:
        self.conversation_history = []
        if existing_history:
            self.conversation_history = ConversationMemory.normalize_raw_conversation_history(existing_history)

    @staticmethod
    def initialise_from_existing_conversation_history(conversation_history: List[Dict[str, str]]) -> 'ConversationMemory':
        processed_history = ConversationMemory.normalize_raw_conversation_history(conversation_history)
        return ConversationMemory(existing_history=processed_history)

    @staticmethod
    def normalize_raw_conversation_history(conversation_history: List[Dict[str, str]]) -> List[ConversationTurn]:
        return [ConversationTurn(**item) for item in conversation_history]
    
    @staticmethod
    def denormalize_conversation_history(conversation_history: List[ConversationTurn]) -> List[Dict[str, str]]:
        return [item.model_dump(by_alias=True) for item in conversation_history]

    def add_object_to_memory(self, object: ConversationTurn) -> None:
        self.conversation_history.append(object)
    
    def get_last_llm_response(self) -> str:
        last_dialogue = self.get_last_dialogue()

        llm_response = ''
        if self.is_dialogue_from_llm(last_dialogue):
            llm_response = last_dialogue.message

        return llm_response

    def is_dialogue_from_llm(self, last_dialogue: ConversationTurn) -> bool:
        return last_dialogue.speaker == Speaker.AGENT

    def get_last_dialogue(self) -> ConversationTurn:
        return self.conversation_history[-1]
