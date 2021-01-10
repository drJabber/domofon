from typing import Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.clients import Client, ClientInDB


class ClientsRepository(BaseRepository):
    async def get_client_by_client_id(self, *, client_id: str) -> ClientInDB:
        client_row = await queries.get_client_by_client_id(
            self.connection,
            client_id=client_id,
        )
        if client_row:
            return ClientInDB(**client_row)

        raise EntityDoesNotExist(
            "client with client_id {0} does not exist".format(client_id),
        )

    async def create_client(
        self,
        *,
        client_id: str,
        client_secret: str,
    ) -> ClientInDB:
        client = ClientInDB(client_id=client_id)
        client.change_secret(client_secret)

        async with self.connection.transaction():
            client_row = await queries.create_new_client(
                self.connection,
                client_id=client.client_id,
                salt=client.salt,
                hashed_secret=client.hashed_secret,
            )

        return client.copy(update=dict(client_row))

    async def update_client( 
        self,
        *,
        client: Client,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> ClientInDB:
        client_in_db = await self.get_client_by_client_id(client_id=client.client_id)

        client_in_db.client_id = client_id or client_in_db.client_id
        if client_secret:
            client_in_db.change_secret(client_secret)

        async with self.connection.transaction():
            client_in_db.updated_at = await queries.update_client_by_client_id(
                self.connection,
                client_id=client.client_id,
                new_client_id=client_in_db.client_id,
                new_salt=client_in_db.salt,
                new_secret=client_in_db.hashed_secret,
            )

        return client_in_db
