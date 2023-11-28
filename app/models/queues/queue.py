from pydantic import BaseModel
from typing import  Optional, Union, Dict, Any

class Queue(BaseModel):
    method: str
    path: str
    collection : str
    data : Optional[Dict[str, Any]]
    e_id : str

class QueueCreate(BaseModel) :
    method: Optional[str]
    path: Optional[str]
    collection : Optional[str]
    data : Optional[Dict[str, Any]]
    e_id : Optional[str]

class QueueGet(BaseModel) :
    method: Optional[str]
    path: Optional[str]
    collection : Optional[str]
    data : Optional[Dict[str, Any]]
    e_id : Optional[str]



