from bson import ObjectId

def encode_object_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))
