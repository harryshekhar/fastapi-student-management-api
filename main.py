from fastapi import FastAPI
from database import engine, Base
import models
from fastapi import Depends
from sqlalchemy.orm import Session 
from database import  engine , Base , SessionLocal
from models import Student
from schemas import StudentCreate
from sqlalchemy import Column, Integer, String
from schemas import UserCreate, UserLogin
from models import User
from auth import (
    hash_password,
    verify_password,
    create_access_token
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "first api project"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = Student(
        name=student.name,
        email=student.email,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.get("/students/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        return {"message": "Student not found"}

    return student

@app.put("/students/{id}")
def update_student(id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == id).first()

    if not db_student:
        return {"message": "Student not found"}

    db_student.name = student.name
    db_student.email = student.email
    db_student.course = student.course

    db.commit()
    db.refresh(db_student)

    return db_student

@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        return {"message": "Student not found"}

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}


@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_pw = hash_password(
        user.password
    )

    new_user = User(
        email=user.email,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered"
    }

@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": "Invalid credentials"
        }

    if not verify_password(
        user.password,
        db_user.password
    ):
        return {
            "message": "Invalid credentials"
        }

    token = create_access_token(
        {"user_id": db_user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }