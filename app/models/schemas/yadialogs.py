from typing import List, Dict, Any, Optional

from pydantic import BaseModel
from app.models.schemas.rwschema import RWSchema

class Interfaces(BaseModel):
    screen: Optional[Dict[Any, Any]]
    payments: Dict[Any, Any]
    account_linking: Dict[Any, Any]

class User(BaseModel):
    user_id: str

class Application(BaseModel):
    application_id: str

class Session(BaseModel):
    message_id: int
    session_id: str
    skill_id: Optional[str]
    user: User
    application: Application
    user_id: str
    new: str

class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interfaces: Interfaces

class Markup(BaseModel):
    dangerous_context: str

class Nlu(BaseModel):
    tokens: List[Any]
    entities: List[Any]
    intents: Dict[Any, Any]


class Request(BaseModel):
    command: str
    original_utterance: str
    nlu: Nlu
    markup: Markup
    type: str


class RequestIn(BaseModel):
    meta: Meta
    session: Session
    request: Request
    version: str


class ResponseSession(BaseModel):
    text: str
    tts: str
    end_session: bool

class ResponseOut(BaseModel):
    version: str
    session: Dict
    response: ResponseSession



