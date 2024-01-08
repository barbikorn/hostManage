from fastapi import FastAPI
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request, Depends, status, Header
from typing import List, Optional, Dict ,Any, Union
from bson import ObjectId
# from app.models.users.user import User,UserUpdate,UserCreate, Token, TokenData
from app.database import get_database_atlas
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi.openapi.utils import get_openapi


from app.models.hosts.route import router as hosts_router
from app.models.queues.route import router as queues_router


print("print from main")
# mongol part
app = FastAPI()

app.include_router(hosts_router, prefix="/hosts", tags=["hosts"])
app.include_router(queues_router, prefix="/queues", tags=["queues"])



# app.include_router(items_router, prefix="/items", tags=["items"])
# app.include_router(shops_router, prefix="/shops", tags=["shops"])


# ---------- My autherize Swagger ----------
# from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
# from fastapi.openapi.models import OAuthFlowAuthorizationCode as OAuthFlowAuthorizationCodeModel
# from fastapi.openapi.models import OAuthFlowPassword as OAuthFlowPasswordModel
# from fastapi.openapi.models import OAuthFlowImplicit as OAuthFlowImplicitModel
# from fastapi.openapi.models import OAuthFlowClientCredentials as OAuthFlowClientCredentialsModel
# from fastapi.openapi.models import OAuthFlowAuthorizationCode as OAuthFlowAuthorizationCodeModel
# from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
# from fastapi.openapi.models import OAuthFlowPassword as OAuthFlowPasswordModel
# from fastapi.openapi.models import OAuthFlowAuthorizationCode as OAuthFlowAuthorizationCodeModel

# # Define your OAuth2 flows
# oauth_flows = OAuthFlowsModel(
#     password=OAuthFlowPasswordModel(tokenUrl="/token"),
#     authorizationCode=OAuthFlowAuthorizationCodeModel(
#         authorizationUrl="/auth", tokenUrl="/token"
#     ),ไ
#     clientCredentials=OAuthFlowClientCredentialsModel(tokenUrl="/token"),
#     implicit=OAuthFlowImplicitModel(authorizationUrl="/auth"),
# )

# # Add the OAuth2 security scheme
# security_schemes = {
#     "OAuth2PasswordBearer": {
#         "type": "oauth2",
#         "flows": oauth_flows,
#     }
# }

# app.openapi = {"security": [{"OAuth2PasswordBearer": []}], "info": {"title": "Your API"}}

# ------------------- Auth System ----------------

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# database_manager = HostDatabaseManager("users")


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def authenticate_user( username: str, password: str, htoken: str):
#     host = htoken
#     collection = database_manager.get_collection(host)
#     user = collection.find_one({"username": username})
#     if not user:
#         return False
#     if not verify_password(password, user['password']):
#         return False
#     return user

# def authenticate_user_email( email: str, password: str):
#     collection = get_database_atlas("WEIS", atlas_uri)["users"]
#     user = collection.find_one({"email": email})
#     if not user:
#         return False
#     if not verify_password(password, user['password']):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(
#         token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(email=username)
#     except JWTError:
#         raise credentials_exception
#     collection = get_database_atlas("WEIS", atlas_uri)["users"]
#     user = collection.find_one({"email": token_data.email})
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @app.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     htoken: Optional[str] = Header(None, description="HToken for additional authentication")
# ):
#     user = authenticate_user(form_data.username, form_data.password,htoken)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user['username']}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# # ------------------ API part ------------
# # Search

# @app.post("/{collection}/aggregate")
# async def aggregate_collection(
#     collection: str,
#     request_data: dict,
#     htoken: Optional[str] = Header(None)
# ):
#     try:
#         pipeline = request_data.get("pipeline", [])

#         if not isinstance(pipeline, list):
#             raise HTTPException(status_code=400, detail="Invalid request format")

#         # Get the database name based on the host or token
#         database_name = database_manager.get_database_name(htoken)

#         if not database_name:
#             raise HTTPException(status_code=404, detail="Database not found for the host")

#         # Get the collection based on the collection name and database name
#         db_collection = database_manager.get_collection(htoken, collection)

#         # Apply additional modifications to the pipeline as needed
#         modified_pipeline = []
#         for stage in pipeline:
#             if "$match" in stage and "_id" in stage["$match"]:
#                 stage["$match"]["_id"] = ObjectId(stage["$match"]["_id"])
#             modified_pipeline.append(stage)

#         result = list(db_collection.aggregate(modified_pipeline))
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.post("/register", response_model=User)
# async def register_user(
#     user_data: UserCreate ,
#     htoken: Optional[str] = Header(None)
#     ):

#     host = htoken
#     collection = database_manager.get_collection(host)
#     user_data_dict = user_data.dict()
#     user_data_dict["password"] = get_password_hash(user_data_dict["password"])
#     result = collection.insert_one(user_data_dict)
     
#     if result.acknowledged:
#         created_user = collection.find_one({"_id": ObjectId(result.inserted_id)})
#         return User(**created_user)
#     else:
#         raise HTTPException(status_code=500, detail="Failed to create user")


# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user


# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)