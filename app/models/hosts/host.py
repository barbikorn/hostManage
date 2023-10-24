from pydantic import BaseModel
from typing import Optional

class Host(BaseModel):
    token: str
    name: str
    databasename: str
    uri : Optional[str]

class HostCreate(BaseModel) :
    token: str
    name: str
    databasename: str
    uri : Optional[str]

class HostGet(BaseModel) :
    id : str
    token: Optional[str]
    name: Optional[str]
    databasename: Optional[str]
    uri : Optional[str]


