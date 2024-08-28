from app.core.llm import LLM
from app.core.memory import ConversationMemory


class Conversation:
    def __init__(self, llm: LLM, conversation_memory: ConversationMemory) -> None:
        self.llm = llm
        self.conversation_memory = conversation_memory
    
    # TODO: Refactor this method. Perhaps give it a better name too.
    # TODO: It will be easier to write cleaner tests after the refactoring. Write unit tests for this after.
    def speak(self, user_message: str) -> str:
        self.conversation_memory.add_user_message_to_memory(user_message)
        llm_payload = self.conversation_memory.get_conversation_history_for_llm_call()
        llm_response = self.llm.call_llm(llm_payload)
        self.conversation_memory.add_llm_message_to_memory(llm_response)

        return llm_response