from app.db.errors import EntityDoesNotExist
from app.db.repositories.doors import DoorsRepository

async def check_door_id_is_taken(repo: DoorsRepository, door_id: str) -> bool:
    try:
        await repo.get_door_by_door_id(door_id=door_id)
    except EntityDoesNotExist:
        return False

    return True

async def check_ext_door_id_is_taken(repo: DoorsRepository, ext_door_id: str) -> bool:
    try:
        await repo.get_door_by_ext_door_id(ext_door_id=ext_door_id)
    except EntityDoesNotExist:
        return False

    return True

