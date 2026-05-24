from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Faculty, Subject, Student, Grade
from schemas import (
    FacultyCreate, FacultyUpdate, FacultyOut,
    SubjectCreate, SubjectUpdate, SubjectOut,
    StudentCreate, StudentUpdate, StudentOut,
    GradeCreate, GradeUpdate, GradeOut,
)

faculty_router = APIRouter(prefix="/faculties", tags=["faculties"])
subject_router = APIRouter(prefix="/subjects", tags=["subjects"])
student_router = APIRouter(prefix="/students", tags=["students"])
grade_router = APIRouter(prefix="/grades", tags=["grades"])


# === Faculty ===

@faculty_router.get("/", response_model=list[FacultyOut])
def list_faculties(db: Session = Depends(get_db)):
    return db.query(Faculty).all()

@faculty_router.get("/{faculty_id}", response_model=FacultyOut)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    obj = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not obj:
        raise HTTPException(404, "faculty not found")
    return obj

@faculty_router.post("/", response_model=FacultyOut, status_code=201)
def create_faculty(data: FacultyCreate, db: Session = Depends(get_db)):
    obj = Faculty(name=data.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@faculty_router.put("/{faculty_id}", response_model=FacultyOut)
def update_faculty(faculty_id: int, data: FacultyUpdate, db: Session = Depends(get_db)):
    obj = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not obj:
        raise HTTPException(404, "faculty not found")
    obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj

@faculty_router.delete("/{faculty_id}", status_code=204)
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    obj = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not obj:
        raise HTTPException(404, "faculty not found")
    db.delete(obj)
    db.commit()


# === Subject ===

@subject_router.get("/", response_model=list[SubjectOut])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@subject_router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    obj = db.query(Subject).filter(Subject.id == subject_id).first()
    if not obj:
        raise HTTPException(404, "subject not found")
    return obj

@subject_router.post("/", response_model=SubjectOut, status_code=201)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    obj = Subject(name=data.name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@subject_router.put("/{subject_id}", response_model=SubjectOut)
def update_subject(subject_id: int, data: SubjectUpdate, db: Session = Depends(get_db)):
    obj = db.query(Subject).filter(Subject.id == subject_id).first()
    if not obj:
        raise HTTPException(404, "subject not found")
    obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj

@subject_router.delete("/{subject_id}", status_code=204)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    obj = db.query(Subject).filter(Subject.id == subject_id).first()
    if not obj:
        raise HTTPException(404, "subject not found")
    db.delete(obj)
    db.commit()


# === Student ===

@student_router.get("/", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@student_router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(404, "student not found")
    return obj

@student_router.post("/", response_model=StudentOut, status_code=201)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    obj = Student(last_name=data.last_name, first_name=data.first_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@student_router.put("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, data: StudentUpdate, db: Session = Depends(get_db)):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(404, "student not found")
    if data.last_name is not None:
        obj.last_name = data.last_name
    if data.first_name is not None:
        obj.first_name = data.first_name
    db.commit()
    db.refresh(obj)
    return obj

@student_router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        raise HTTPException(404, "student not found")
    db.delete(obj)
    db.commit()


# === Grade ===

@grade_router.get("/", response_model=list[GradeOut])
def list_grades(db: Session = Depends(get_db)):
    return db.query(Grade).all()

@grade_router.get("/{grade_id}", response_model=GradeOut)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    obj = db.query(Grade).filter(Grade.id == grade_id).first()
    if not obj:
        raise HTTPException(404, "grade not found")
    return obj

@grade_router.post("/", response_model=GradeOut, status_code=201)
def create_grade(data: GradeCreate, db: Session = Depends(get_db)):
    obj = Grade(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@grade_router.put("/{grade_id}", response_model=GradeOut)
def update_grade(grade_id: int, data: GradeUpdate, db: Session = Depends(get_db)):
    obj = db.query(Grade).filter(Grade.id == grade_id).first()
    if not obj:
        raise HTTPException(404, "grade not found")
    obj.grade = data.grade
    db.commit()
    db.refresh(obj)
    return obj

@grade_router.delete("/{grade_id}", status_code=204)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    obj = db.query(Grade).filter(Grade.id == grade_id).first()
    if not obj:
        raise HTTPException(404, "grade not found")
    db.delete(obj)
    db.commit()


# === Analytics ===

analytics_router = APIRouter(prefix="/analytics", tags=["analytics"])

@analytics_router.get("/avg-grade/{faculty_name}")
def avg_grade(faculty_name: str, db: Session = Depends(get_db)):
    result = (
        db.query(func.avg(Grade.grade))
        .join(Faculty, Faculty.id == Grade.faculty_id)
        .filter(Faculty.name == faculty_name)
        .scalar()
    )
    if result is None:
        raise HTTPException(404, "faculty not found or no grades")
    return {"faculty": faculty_name, "avg_grade": round(float(result), 2)}
