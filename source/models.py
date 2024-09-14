from pydantic import BaseModel
from typing import Optional, List

class KnowledgeTripletItem(BaseModel):
    item: str
    info: str = ''
    url: str = ''
    type_: List[str] = []

class KnowledgeTriplet(BaseModel):
    subject: KnowledgeTripletItem
    object: KnowledgeTripletItem
    relation: KnowledgeTripletItem