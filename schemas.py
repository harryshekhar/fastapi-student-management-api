from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    email: str
    course: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str