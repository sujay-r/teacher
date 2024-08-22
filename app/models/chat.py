from app.models.enums import Speaker
from pydantic import BaseModel, Field, field_validator, ValidationInfo

class Message(BaseModel):
    message: str


class Dialogue(BaseModel):
    speaker: str = Field(..., alias='role')
    message: str = Field(..., alias='content')

    @field_validator("speaker")
    @classmethod
    def check_speaker_type(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            speaker_values = [member.value for member in Speaker]
            is_valid_speaker_type = v in speaker_values
            assert is_valid_speaker_type, f"speaker must be one of {speaker_values}"
        return v
