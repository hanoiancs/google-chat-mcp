from pydantic import BaseModel, Field
from datetime import datetime


class SenderModel(BaseModel):
    id: str
    name: str
    display_name: str


class MessageQuoteModel(BaseModel):
    name: str
    text: str
    create_time: str
    type: str


class MessageThreadModel(BaseModel):
    name: str


class MessageModel(BaseModel):
    name: str
    text: str
    create_time: str
    sender: SenderModel | None = None
    thread: MessageThreadModel | None = None
    quote: MessageQuoteModel | None = None


class SpaceModel(BaseModel):
    name: str
    display_name: str


class MemberModel(BaseModel):
    id: str
    name: str
    member_name: str = ""
    display_name: str = ""
    type: str = ""
    role: str = ""
    state: str = ""
