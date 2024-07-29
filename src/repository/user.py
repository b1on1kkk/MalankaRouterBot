from pydantic import BaseModel

class User(BaseModel):
    id: int
    connection_type: str