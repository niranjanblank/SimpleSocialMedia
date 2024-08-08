from pydantic import BaseModel
from typing import Optional

## Board Schemas
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


## User Schemas
class UserBase(BaseModel):
    """ Base class for other schemas """
    username: str
    email: str


class UserCreate(UserBase):
    """ Fields needed when registering user(in this case username, email and password) """
    password: str


class UserRead(UserBase):
    """ Fields returned when querying user details"""
    id: int


## BoardList Schemas
class BoardList(BaseModel):
    """Base class for other list schemas"""
    title: str
    board_id: int
    order: Optional[int] = None


class BoardListCreate(BoardList):
    """Fields needed when creating a board lists"""
    pass


class BoardListRead(BoardList):
    """Fields returned when reading board lists"""
    id: int


class BoardListUpdate(BaseModel):
    title: str | None = None


## ListCard Schemas
class ListCardBase(BaseModel):
    """Base class for the cards in a lists"""
    title: str
    desc: str
    list_id: int
    order: Optional[int] = None

class ListCardCreate(ListCardBase):
    """ Attributes required to create a card in a list """
    pass


class ListCardRead(ListCardBase):
    """ Attributes returned when reading list card """
    id: int
    pass

# for jwt
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    user_id: int

# Relationships
class UserReadWithBoard(UserBase):
    boards: list[BoardRead] = []
    id: int


class BoardReadWithOwner(BoardBase):
    id: int
    owner: UserRead

class BoardListWithCards(BoardListRead):
    list_cards: list[ListCardRead]=[]

class BoardReadWithListAndCard(BoardRead):
    board_lists: list[BoardListWithCards] = []

