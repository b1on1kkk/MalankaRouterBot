from pydantic import BaseModel

class User(BaseModel):
    id_hash: str
    connection_type: str