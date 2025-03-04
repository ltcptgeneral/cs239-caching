from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    name: str | None = None
    followers: int | None = None
    bio: str | None = None
    posts: str | None = None
    friends: list | None = None