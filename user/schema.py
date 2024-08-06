from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    email: EmailStr = Field()
    password: str = Field()

    class Config:
        json_schema_extra = {
            "example": {"email": "test@gmail.com", "password": "testpassword"}
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field()
    password: str = Field()

    class Config:
        json_schema_extra = {
            "example": {"email": "test@gmail.com", "password": "testpassword"}
        }
