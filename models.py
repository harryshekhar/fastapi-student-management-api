from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = Column(String, default="student")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    students = relationship(
        "Student",
        back_populates="user"
    )


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    description = Column(String)

    students = relationship(
        "Student",
        back_populates="department"
    )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    course = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="students"
    )

    department = relationship(
        "Department",
        back_populates="students"
    )