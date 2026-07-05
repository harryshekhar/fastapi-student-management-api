from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    course = Column(String)

    owner_id = Column(
        Integer, 
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="students"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    students = relationship(
        "Student",
        back_populates="owner"
    )