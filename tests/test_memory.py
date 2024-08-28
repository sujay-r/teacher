from app.core.memory import ConversationMemory
from app.models.chat import ConversationTurn
from app.models.enums import Speaker


class TestConversationMemory:

    def test_initialization_with_no_history(self):
        memory = ConversationMemory()
        assert memory.conversation_history == []

    def test_initialization_with_existing_history(self):
        existing_history = [
            {"role": Speaker.HUMAN.value, "content": "Hello!"},
            {"role": Speaker.AGENT.value, "content": "Hi! How can I help you?"},
        ]
        memory = ConversationMemory.initialise_from_existing_conversation_history(existing_history)
        assert len(memory.conversation_history) == 2
        assert memory.conversation_history[0].speaker == Speaker.HUMAN.value
        assert memory.conversation_history[1].speaker == Speaker.AGENT.value

    def test_add_user_message_to_memory(self):
        memory = ConversationMemory()
        memory.add_user_message_to_memory("Hello!")
        assert len(memory.conversation_history) == 1
        assert memory.conversation_history[0].speaker == Speaker.HUMAN.value
        assert memory.conversation_history[0].message == "Hello!"

    def test_add_llm_message_to_memory(self):
        memory = ConversationMemory()
        memory.add_llm_message_to_memory("Hi! How can I help you?")
        assert len(memory.conversation_history) == 1
        assert memory.conversation_history[0].speaker == Speaker.AGENT.value
        assert memory.conversation_history[0].message == "Hi! How can I help you?"

    def test_denormalize_conversation_history(self):
        conversation_turns = [
            ConversationTurn(role=Speaker.HUMAN.value, content="Hello!"),
            ConversationTurn(
                role=Speaker.AGENT.value, content="Hi! How can I help you?"
            ),
        ]
        denormalized = ConversationMemory.denormalize_conversation_history(
            conversation_turns
        )
        assert len(denormalized) == 2
        assert denormalized[0]["role"] == Speaker.HUMAN.value
        assert denormalized[0]["content"] == "Hello!"
        assert denormalized[1]["role"] == Speaker.AGENT.value
        assert denormalized[1]["content"] == "Hi! How can I help you?"
