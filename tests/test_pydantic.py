import pytest
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ValidationInfo, ValidationError

class DemoEnum(Enum):
    CLASS_A = 'a'
    CLASS_B = 'b'
    CLASS_C = 'c'


class DemoModel(BaseModel):
    field_a: str = Field(..., alias='a')
    field_b: str = Field(..., alias='b')

    @field_validator('field_a')
    @classmethod
    def check_field_a(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            enum_values = [member.value for member in DemoEnum]
            is_valid_enum_value = v in enum_values
            assert is_valid_enum_value, f'field_a must be one of {enum_values}'


def test_enum_values():
    enum_values = [member.value for member in DemoEnum]
    assert enum_values == ['a', 'b', 'c']

def test_pydantic_validator_true():
    DemoModel(a='a', b='d')

def test_pydantic_validator_false():
    with pytest.raises(ValidationError):
        DemoModel(a='d', b='a')
