from pydantic import BaseModel
from typing import Optional

class KnowledgeTripletItem(BaseModel):
    item: str
    info: str = ''
    url: str = ''
    type_: str = ''

class KnowledgeTriplet(BaseModel):
    subject: KnowledgeTripletItem
    object: KnowledgeTripletItem
    relation: KnowledgeTripletItem