from typing import Dict, Optional, List, Any
from app.database import get_database_atlas
from fastapi import HTTPException, APIRouter, Depends , Request, Query
from pymongo.collection import Collection
from pymongo import errors
from pydantic import BaseModel
from bson import ObjectId

from app.models.queues.queue import Queue, QueueGet, QueueCreate

router = APIRouter()
collection_name = "queues"
atlas_uri = "mongodb+srv://doadmin:k2R0165xp4G8iV3E@host-manager-a6c7287d.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection = get_database_atlas("hosts", atlas_uri)[collection_name]



@router.post("/", response_model=QueueGet)
def create_queue(queue_data: QueueCreate):
    try:
        # Create a unique index on the 'token' field
        collection.create_index("token", unique=True)
        
        # Insert the queue data into the collection
        result = collection.insert_one(queue_data.dict())
        
        if result.acknowledged:
            queue_id = str(result.inserted_id)
            return QueueGet(id=queue_id, **queue_data.dict())
        else:
            raise HTTPException(status_code=500, detail="Failed to create queue")
    except errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Queue with the same token already exists")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_queues():
    queues = []
    for queue in collection.find():
        queue_id = str(queue.pop('_id'))
        queue["id"] = queue_id
        queues.append(queue)
    return queues

@router.get("/{queue_id}", response_model=QueueGet)
def get_queue(queue_id: str):
    queue = collection.find_one({"_id": ObjectId(queue_id)})
    if queue:
        return Queue(id=str(queue["_id"]), **queue)
    else:
        raise HTTPException(status_code=404, detail="Queue not found")

@router.get("/filters/", response_model=List[Queue])
async def get_queue_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Queue]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    queues = []
    async for queue in cursor:
        queues.append(Queue(id=str(queue["_id"]), **queue))
    return queues

@router.put("/{queue_id}", response_model=Queue,include_in_schema=True)
def update_queue(queue_id: str, queue_data: Queue):
    result = collection.update_one({"_id": ObjectId(queue_id)}, {"$set": queue_data.dict()})
    if result.modified_count == 1:
        updated_queue = collection.find_one({"_id": ObjectId(queue_id)})
        return Queue(id=str(updated_queue["_id"]), **updated_queue)
    else:
        raise HTTPException(status_code=404, detail="Queue not found")

@router.delete("/{queue_id}",include_in_schema=False)
def delete_queue(queue_id: str):
    result = collection.delete_one({"_id": ObjectId(queue_id)})
    if result.deleted_count == 1:
        return {"message": "Queue deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Queue not found")


