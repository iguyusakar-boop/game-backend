from pydantic import BaseModel

class ActionLogIn(BaseModel):
    user_id: int
    action_type: str
    value: int = 1