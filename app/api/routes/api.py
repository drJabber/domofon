from fastapi import APIRouter

# from app.api.routes import authentication, users
from app.api.routes import doors 

router = APIRouter()

# router.include_router(authentication.router, tags=["authentication"], prefix="/client")
# router.include_router(users.router, tags=["users"], prefix="/user")

router.include_router(doors.router, tags=["domofon"], prefix="/domofon")