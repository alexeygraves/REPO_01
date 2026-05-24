from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal, engine
from models import Base

Base.metadata.create_all(engine)

app = FastAPI(title="Students CRUD API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- data loading ---

@app.post("/load-csv", tags=["data"])
def load_csv(db: Session = Depends(get_db)):
    crud.load_from_csv(db)
    return {"status": "loaded"}


# --- faculties ---

@app.post("/faculties/", response_model=schemas.FacultyOut, tags=["faculties"])
def create_faculty(body: schemas.FacultyCreate, db: Session = Depends(get_db)):
    return crud.create_faculty(db, body.name)

@app.get("/faculties/", response_model=list[schemas.FacultyOut], tags=["faculties"])
def list_faculties(db: Session = Depends(get_db)):
    return crud.list_faculties(db)

@app.get("/faculties/{faculty_id}", response_model=schemas.FacultyOut, tags=["faculties"])
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    obj = crud.get_faculty(db, faculty_id)
    if not obj:
        raise HTTPException(404, "faculty not found")
    return obj

@app.put("/faculties/{faculty_id}", response_model=schemas.FacultyOut, tags=["faculties"])
def update_faculty(faculty_id: int, body: schemas.FacultyUpdate, db: Session = Depends(get_db)):
    obj = crud.update_faculty(db, faculty_id, body.name)
    if not obj:
        raise HTTPException(404, "faculty not found")
    return obj

@app.delete("/faculties/{faculty_id}", tags=["faculties"])
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    if not crud.delete_faculty(db, faculty_id):
        raise HTTPException(404, "faculty not found")
    return {"deleted": faculty_id}


# --- subjects ---

# уникальный путь должен быть выше /{subject_id}, иначе FastAPI попытается привести "unique" к int
@app.get("/subjects/unique", tags=["subjects"])
def unique_subjects(db: Session = Depends(get_db)):
    return {"subjects": crud.list_unique_subjects(db)}

@app.post("/subjects/", response_model=schemas.SubjectOut, tags=["subjects"])
def create_subject(body: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, body.name)

@app.get("/subjects/", response_model=list[schemas.SubjectOut], tags=["subjects"])
def list_subjects(db: Session = Depends(get_db)):
    return crud.list_subjects(db)

@app.get("/subjects/{subject_id}", response_model=schemas.SubjectOut, tags=["subjects"])
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    obj = crud.get_subject(db, subject_id)
    if not obj:
        raise HTTPException(404, "subject not found")
    return obj

@app.put("/subjects/{subject_id}", response_model=schemas.SubjectOut, tags=["subjects"])
def update_subject(subject_id: int, body: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    obj = crud.update_subject(db, subject_id, body.name)
    if not obj:
        raise HTTPException(404, "subject not found")
    return obj

@app.delete("/subjects/{subject_id}", tags=["subjects"])
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    if not crud.delete_subject(db, subject_id):
        raise HTTPException(404, "subject not found")
    return {"deleted": subject_id}


# --- students ---

@app.post("/students/", response_model=schemas.StudentOut, tags=["students"])
def create_student(body: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, body.last_name, body.first_name)

@app.get("/students/", response_model=list[schemas.StudentOut], tags=["students"])
def list_students(
    faculty: str = Query(None, description="фильтр по факультету"),
    db: Session = Depends(get_db)
):
    if faculty:
        return crud.list_students_by_faculty(db, faculty)
    return crud.list_students(db)

@app.get("/students/low-grades", tags=["students"])
def students_low_grades(
    subject: str = Query(..., description="название курса"),
    threshold: int = Query(30, description="порог оценки (не включительно)"),
    db: Session = Depends(get_db)
):
    return crud.list_students_low_grade(db, subject, threshold)

@app.get("/students/{student_id}", response_model=schemas.StudentOut, tags=["students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    obj = crud.get_student(db, student_id)
    if not obj:
        raise HTTPException(404, "student not found")
    return obj

@app.put("/students/{student_id}", response_model=schemas.StudentOut, tags=["students"])
def update_student(student_id: int, body: schemas.StudentUpdate, db: Session = Depends(get_db)):
    obj = crud.update_student(db, student_id, body.last_name, body.first_name)
    if not obj:
        raise HTTPException(404, "student not found")
    return obj

@app.delete("/students/{student_id}", tags=["students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(404, "student not found")
    return {"deleted": student_id}


# --- grades ---

@app.post("/grades/", response_model=schemas.GradeOut, tags=["grades"])
def create_grade(body: schemas.GradeCreate, db: Session = Depends(get_db)):
    return crud.create_grade(db, body.student_id, body.faculty_id, body.subject_id, body.grade)

@app.get("/grades/", response_model=list[schemas.GradeOut], tags=["grades"])
def list_grades(db: Session = Depends(get_db)):
    return crud.list_grades(db)

@app.get("/grades/{grade_id}", response_model=schemas.GradeOut, tags=["grades"])
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    obj = crud.get_grade(db, grade_id)
    if not obj:
        raise HTTPException(404, "grade not found")
    return obj

@app.put("/grades/{grade_id}", response_model=schemas.GradeOut, tags=["grades"])
def update_grade(grade_id: int, body: schemas.GradeUpdate, db: Session = Depends(get_db)):
    obj = crud.update_grade(db, grade_id, body.grade)
    if not obj:
        raise HTTPException(404, "grade not found")
    return obj

@app.delete("/grades/{grade_id}", tags=["grades"])
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    if not crud.delete_grade(db, grade_id):
        raise HTTPException(404, "grade not found")
    return {"deleted": grade_id}


# --- analytics ---

@app.get("/analytics/avg-grade", tags=["analytics"])
def avg_grade_by_faculty(
    faculty: str = Query(..., description="название факультета"),
    db: Session = Depends(get_db)
):
    avg = crud.avg_grade_by_faculty(db, faculty)
    if avg is None:
        raise HTTPException(404, "faculty not found or no grades")
    return {"faculty": faculty, "avg_grade": avg}


# --- export (бонусное задание) ---

@app.get("/export/csv", tags=["data"])
def export_csv(db: Session = Depends(get_db)):
    content = crud.export_to_csv(db)
    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students_export.csv"}
    )
