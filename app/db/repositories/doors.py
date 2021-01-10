from typing import Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.doors import Door, DoorInDB


class DoorsRepository(BaseRepository):
    async def get_door_by_door_id(self, *, door_id: str) -> DoorInDB:
        door_row = await queries.get_door_by_door_id(
            self.connection,
            door_id=door_id,
        )
        if door_row:
            return DoorInDB(**door_row)

        raise EntityDoesNotExist(
            "door with door_id {0} does not exist".format(door_id),
        )

    async def get_door_by_ext_door_id(self, *, ext_door_id: str) -> DoorInDB:
        door_row = await queries.get_door_by_ext_door_id(
            self.connection,
            ext_door_id=ext_door_id,
        )
        if door_row:
            return DoorInDB(**door_row)

        raise EntityDoesNotExist(
            "door with ext_door_id {0} does not exist".format(ext_door_id),
        )

    async def create_door(
        self,
        *,
        door_id: str,
        ext_door_id: str,
        ext_user: str,
        ext_password : str
    ) -> DoorInDB:
        door = DoorInDB(door_id=door_id, ext_door_id=ext_door_id, ext_user=ext_user, ext_password=ext_password)

        async with self.connection.transaction():
            door_row = await queries.create_new_door(
                self.connection,
                door_id=door.door_id,
                ext_door_id=door.ext_door_id,
                ext_user=door.ext_user,
                ext_password=door.ext_password,
            )

        return door.copy(update=dict(door_row))

    async def update_client( 
        self,
        *,
        door: Door,
        door_id: Optional[str] = None,
        ext_door_id: Optional[str] = None,
        ext_user:  Optional[str] = None,
        ext_password: Optional[str] = None
    ) -> DoorInDB:
        door_in_db = await self.get_door_by_door_id(door_id=door.door_id)

        door_in_db.door_id = door_id or door_in_db.door_id
        door_in_db.ext_id = ext_door_id or door_in_db.ext_door_id
        door_in_db.ext_user = ext_user or door_in_db.ext_user
        door_in_db.ext_password = ext_password or door_in_db.ext_password

        async with self.connection.transaction():
            door_in_db.updated_at = await queries.update_door_by_door_id(
                self.connection,
                door_id=door.door_id,
                new_door_id=door_in_db.door_id,
                new_ext_id=door_in_db.ext_door_id,
                new_ext_user=door_in_db.ext_user,
                new_ext_password=door_in_db.ext_password
            )

        return door_in_db
