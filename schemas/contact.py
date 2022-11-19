from uuid import uuid1
from pydantic import BaseModel
from typing import Optional, List

class Contact(BaseModel):
    _id: Optional[str] = uuid1()
    id: Optional[str] = uuid1()
    name: str
    phone: str
    addressLines: List[str]