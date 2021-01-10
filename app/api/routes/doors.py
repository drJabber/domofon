from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.resources import strings
from app.db.errors import EntityDoesNotExist
from app.api.dependencies.database import get_repository
from app.db.repositories.doors import DoorsRepository
from app.models.domain.doors  import Door      
from app.models.schemas.doors  import (DoorIn,      
    DoorInResponse,
    DoorInCreate
)
from app.services.doors import check_door_id_is_taken, check_ext_door_id_is_taken

router = APIRouter()

@router.post("/open", response_model=DoorInResponse, name="door:open")
async def open(
    door_in: DoorIn = Body(..., embed=True, alias="door"),
    doors_repo: DoorsRepository = Depends(get_repository(DoorsRepository))
) -> DoorInResponse:
    wrong_door_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_DOOR,
    )
    cant_open_error = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=strings.CANT_OPEN_DOOR,
    )

    try:
        door = await doors_repo.get_door_by_door_id(door_id=door_in.door_id)

    except EntityDoesNotExist as existence_error:
        raise wrong_door_error

    if not door.open():
        raise cant_open_error

    return DoorInResponse(
        door=Door(door_id=door.door_id)
    )

@router.post("/register", 
    status_code=status.HTTP_201_CREATED,
    response_model=DoorInResponse, 
    name="door:register")
async def register(
    door_create: DoorInCreate  = Body(..., embed=True, alias="door"),
    doors_repo: DoorsRepository = Depends(get_repository(DoorsRepository))
) -> DoorInResponse:
    if await check_door_id_is_taken(doors_repo, door_create.door_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.DOOR_TAKEN,
        )

    if await check_ext_door_id_is_taken(doors_repo, door_create.ext_door_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.DOOR_TAKEN,
        )
    
    door = await doors_repo.create_door(**door_create.dict())

    return DoorInResponse(
        door=Door(door_id=door.door_id)
    )
