from pydantic import BaseModel, Field, ValidationInfo, field_validator

from app.models.enums import Speaker


class Message(BaseModel):
    message: str = Field(..., alias='content')


class ConversationTurn(Message):
    speaker: str = Field(..., alias='role')

    @field_validator("speaker")
    @classmethod
    def check_speaker_type(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            speaker_values = [member.value for member in Speaker]
            is_valid_speaker_type = v in speaker_values
            assert (
                is_valid_speaker_type
            ), f'Invalid speaker type "{v}". Must be one of {speaker_values}'
        return v
