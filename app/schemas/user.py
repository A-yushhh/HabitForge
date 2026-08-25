from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, Field, EmailStr, field_validator,ConfigDict

class UserCreate(BaseModel):
    username: str = Field(min_length=5,max_length=50,)
    email: EmailStr
    password: str = Field(min_length=8,max_length=50,)
    timezone: str="UTC"
    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError:
            raise ValueError("Invalid timezone")
        return value
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    timezone: str
    model_config = ConfigDict(
        from_attributes=True
    )