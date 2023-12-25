from pydantic import BaseModel


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
