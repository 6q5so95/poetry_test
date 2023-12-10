from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator,
)

# validator packageから呼び出し
## field validator
from validator.field_validator import (
    name_must_contain_space,
    user_name_alphabetic,
)

## model validator
from validator.model_validator import (
    check_password_match,
)

class UserModel(BaseModel):
    name: str = Field(...)
    username: str = Field(...)
    password1: str = Field(...)
    password2: str = Field(...)
    
    # 挙動定義
    model_config = ConfigDict(
        case_sensitive=True,
        validate_assignment=True,
        strict=True,
    )

    # field validator
    @field_validator
    @classmethod
    def name_must_contain_space(cls, v:str) -> str:
        return name_must_contain_space(v)

    @field_validator
    @classmethod
    def user_name_alphabetic(cls, v:str) -> str:
        return user_name_alphabetic(v)
    
    # model validator
    @model_validator(mode='after')
    def check_password_match(self) -> 'UserModel':
        check_password_match(self.password1, self.password2)
        return self

class ExcelSampleModel(BaseModel):
    No: int = Field(..., gt=0)
    a: str = Field(...)
    b: str = Field(...)
    c: str = Field(...)
    d: str = Field(...)
    e: str = Field(...)
    f str = Field(...)
    g: str = Field(...)
    h str = Field(...)
    i: str = Field(...)
    j: str = Field(...)

    # 挙動定義
    model_config = ConfigDict(
        case_sensitive=True,
        validate_assignment=True,
        strict=True,
    )

    @field_validator('a')
    @classmethod
    def is_alphabet(cls, v:str) -> str:
        if not v.is_alpha():
            raise ValueError('field_a must be alphabet')
        return v

    @field_validator('b')
    @classmethod
    def is_alphabet(cls, v:str) -> str:
        if not v.is_alpha():
            raise ValueError('field_b must be alphabet')
        return v