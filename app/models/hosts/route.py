from typing import Dict, Optional, List, Any
from app.database import get_database_atlas
from fastapi import HTTPException, APIRouter, Depends , Request, Query
from host_manager import HostDatabaseManager
from pymongo.collection import Collection
from pymongo import errors
from pydantic import BaseModel
from bson import ObjectId

from app.models.hosts.host import Host, HostGet, HostCreate

router = APIRouter()
collection_name = "hosts"
atlas_uri = "mongodb+srv://doadmin:k2R0165xp4G8iV3E@host-manager-a6c7287d.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection = get_database_atlas("hosts", atlas_uri)[collection_name]

host_db_manager = HostDatabaseManager(collection_name)


@router.post("/", response_model=HostGet)
def create_host(host_data: HostCreate):
    try:
        # Create a unique index on the 'token' field
        collection.create_index("token", unique=True)
        
        # Insert the host data into the collection
        result = collection.insert_one(host_data.dict())
        
        if result.acknowledged:
            host_id = str(result.inserted_id)
            return HostGet(id=host_id, **host_data.dict())
        else:
            raise HTTPException(status_code=500, detail="Failed to create host")
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Host with the same token already exists")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_hosts():
    hosts = []
    for host in collection.find():
        host_id = str(host.pop('_id'))
        host["id"] = host_id
        hosts.append(host)
    return hosts

@router.get("/{host_id}", response_model=HostGet)
def get_host(host_id: str):
    host = collection.find_one({"_id": ObjectId(host_id)})
    if host:
        return Host(id=str(host["_id"]), **host)
    else:
        raise HTTPException(status_code=404, detail="Host not found")

@router.get("/filters/", response_model=List[Host])
async def get_host_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Host]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    hosts = []
    async for host in cursor:
        hosts.append(Host(id=str(host["_id"]), **host))
    return hosts

@router.put("/{host_id}", response_model=Host,include_in_schema=True)
def update_host(host_id: str, host_data: Host):
    result = collection.update_one({"_id": ObjectId(host_id)}, {"$set": host_data.dict()})
    if result.modified_count == 1:
        updated_host = collection.find_one({"_id": ObjectId(host_id)})
        return Host(id=str(updated_host["_id"]), **updated_host)
    else:
        raise HTTPException(status_code=404, detail="Host not found")

@router.delete("/{host_id}",include_in_schema=False)
def delete_host(host_id: str):
    result = collection.delete_one({"_id": ObjectId(host_id)})
    if result.deleted_count == 1:
        return {"message": "Host deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Host not found")


