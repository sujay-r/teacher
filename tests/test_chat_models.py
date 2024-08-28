import pytest
from pydantic import ValidationError
from app.models.chat import ConversationTurn
from app.models.enums import Speaker


def test_successful_conversation_turn_creation():
    user_turn = ConversationTurn(role=Speaker.HUMAN.value, content='hello!')


def test_conversation_turn_content_validation_error():
    with pytest.raises(ValidationError):
        user_turn = ConversationTurn(role=Speaker.HUMAN.value, content=5)


def test_conversation_turn_speaker_validation_error():
    with pytest.raises(ValidationError):
        incorrect_turn = ConversationTurn(role='random', content='hello')