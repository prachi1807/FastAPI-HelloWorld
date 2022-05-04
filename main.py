from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException

from models import Gender, User, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("9bc18105-1aea-4d6e-ab32-01599ce00ea9"), 
        first_name="Prachi", 
        last_name="Chodankar",
        gender=Gender.female,
        roles = [Role.student]
    ),
    User(
        id=UUID("be9852e6-caba-415c-be10-17d67def0cf9"), 
        first_name="Prathamesh", 
        last_name="Chodankar",
        gender=Gender.male,
        roles = [Role.admin, Role.user]
    )
]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return 
    raise HTTPException(
        status_code= 404,
        detail= f"User with id: {user_id} does not exist"
    )
    

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles

    raise HTTPException(
        status_code=404,
        detail= f"User with id {user_id} does not exist"
    )            
