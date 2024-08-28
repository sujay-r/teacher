from app.models import ConversationTurnFactory, SimpleMessageFactory
from app.models.chat import ConversationTurn, Message
from app.models.enums import Speaker


def test_create_message_simple():
    # Test for SimpleMessageFactory.create_message
    content = "Hello, World!"
    message = SimpleMessageFactory.create_message(content)

    assert isinstance(message, Message)
    assert message.message == content


def test_create_message_array_simple():
    # Test for SimpleMessageFactory.create_message_array
    content_list = ["Hello", "World", "Test"]
    messages = SimpleMessageFactory.create_message_array(content_list)

    assert isinstance(messages, list)
    assert len(messages) == len(content_list)
    assert all(isinstance(msg, Message) for msg in messages)
    assert [msg.message for msg in messages] == content_list


def test_create_message_conversation_turn():
    # Test for ConversationTurnFactory.create_message
    content = "Hi there!"
    role = Speaker.HUMAN.value
    message = ConversationTurnFactory.create_message(content, role)

    assert isinstance(message, ConversationTurn)
    assert message.message == content
    assert message.speaker == role


def test_create_message_array_conversation_turn():
    # Test for ConversationTurnFactory.create_message_array
    messages_input = [
        {"content": "Hello", "role": Speaker.HUMAN.value},
        {"content": "Hi", "role": Speaker.AGENT.value},
        {"content": "How are you?", "role": Speaker.HUMAN.value},
    ]
    messages = ConversationTurnFactory.create_message_array(messages_input)

    assert isinstance(messages, list)
    assert len(messages) == len(messages_input)
    assert all(isinstance(msg, ConversationTurn) for msg in messages)
    assert [msg.message for msg in messages] == [m["content"] for m in messages_input]
    assert [msg.speaker for msg in messages] == [m["role"] for m in messages_input]
