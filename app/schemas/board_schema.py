from pydantic import BaseModel


class BoardBase(BaseModel):
    """ Base class for other schemas """
    title: str
    description: str
    owner_id: int


class BoardCreate(BoardBase):
    """ Fields needed when creating a board"""
    pass


class BoardRead(BoardBase):
    """ Fields returned when querying board details"""
    id: int


class BoardUpdate(BoardBase):
    """ Fields that can be updated in a board """
    title: str | None = None
    description: str | None = None
    owner_id: int | None = None
