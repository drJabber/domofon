from typing import Any, Dict
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
from app.models.schemas.yadialogs import (RequestIn, 
    ResponseOut,
    ResponseSession,
    )

from app.services.utils import get_positive_open_response_for_yd, get_positive_open_tts_response_for_yd

from app.services.doors import check_door_id_is_taken, check_ext_door_id_is_taken
from app.services.domofon import Domofon

router = APIRouter()
domofon = Domofon()

@router.post("/aliceopen", response_model=ResponseOut, name="door:open")
async def alice_open(
    door_id: str,
    alice_in: RequestIn , #= Body(..., embed=True, alias="request"),
    # rq : Dict[Any, Any],
    doors_repo: DoorsRepository = Depends(get_repository(DoorsRepository))
) -> ResponseOut:
    wrong_door_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_DOOR,
    )
    cant_open_error = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=strings.CANT_OPEN_DOOR,
    )
    # alice_in = RequestIn()
    try:
        # door = await doors_repo.get_door_by_door_id(door_id=door_in.door_id)
        door = await doors_repo.get_door_by_door_id(door_id=door_id)

    except EntityDoesNotExist as existence_error:
        raise wrong_door_error

    if not await domofon.open(door):
        raise cant_open_error
    else:
        await doors_repo.update_door(door=Door(door_id=door.door_id), \
            ext_door_id=door.ext_door_id, \
            access_token=door.access_token, \
            refresh_token=door.refresh_token, \
            access_token_expires=door.access_token_expires \
        )

    return ResponseOut(
        version=alice_in.version,
        session=alice_in.session,
        response=ResponseSession(
            text=get_positive_open_response_for_yd(),
            tts=get_positive_open_tts_response_for_yd(),
            end_session="True")
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
    
    door = await doors_repo.create_door(**door_create.dict())

    return DoorInResponse(
        door=Door(door_id=door.door_id)
    )
