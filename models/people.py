from uuid import UUID, uuid1
from pydantic import BaseModel
from typing import Optional, List

class People(BaseModel):
    id: Optional[str] = uuid1()
    name: str
    phone: str
    addressLines: List[str]