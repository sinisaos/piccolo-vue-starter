from typing import Optional

from pydantic import BaseModel


# token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# user schema
class UserModelIn(BaseModel):
    username: str
    email: str
    password: str


class UserModelOut(BaseModel):
    id: int
    username: str
    email: str
