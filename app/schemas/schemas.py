from pydantic import BaseModel


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


class BoardListCreate(BoardList):
    """Fields needed when creating a board lists"""
    pass


class BoardListRead(BoardList):
    """Fields returned when reading board lists"""
    id: int


class BoardListUpdate(BaseModel):
    title: str | None = None


# Relationships
class UserReadWithBoard(UserBase):
    boards: list[BoardRead] = []
    id: int


class BoardReadWithOwner(BoardBase):
    id: int
    owner: UserRead
