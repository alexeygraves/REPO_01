from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import crud
import schemas
import cache
from database import SessionLocal, engine
from models import Base

Base.metadata.create_all(engine)

app = FastAPI(title="Students API — Background Tasks & Redis Cache")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- background task helpers ---
# важно: создаём свою сессию внутри задачи — сессия из request уже закрыта к моменту выполнения

def _bg_load_csv(filepath: str):
    db = SessionLocal()
    try:
        crud.load_from_csv(db, filepath)
        cache.flush_all()
    finally:
        db.close()


def _bg_bulk_delete_students(ids: list[int]):
    db = SessionLocal()
    try:
        crud.bulk_delete_students(db, ids)
        cache.invalidate("students:*")
        cache.invalidate("grades:*")
        cache.invalidate("analytics:*")
    finally:
        db.close()


def _bg_bulk_delete_grades(ids: list[int]):
    db = SessionLocal()
    try:
        crud.bulk_delete_grades(db, ids)
        cache.invalidate("grades:*")
        cache.invalidate("analytics:*")
        cache.invalidate("students:low*")
    finally:
        db.close()


# =============================================================================
# data loading
# =============================================================================

@app.post("/load-csv", tags=["data"])
def load_csv_sync(db: Session = Depends(get_db)):
    """Синхронная загрузка — удобно для первого запуска."""
    crud.load_from_csv(db)
    cache.flush_all()
    return {"status": "loaded"}


@app.post("/load-csv-background", tags=["data"])
def load_csv_background(
    background_tasks: BackgroundTasks,
    filepath: str = Query("students.csv", description="путь к csv-файлу")
):
    """Шаг 1: запускает загрузку csv как фоновую задачу, сразу возвращает ответ."""
    background_tasks.add_task(_bg_load_csv, filepath)
    return {"status": "loading started", "file": filepath}


# =============================================================================
# bulk delete (Шаг 2)
# =============================================================================

@app.delete("/students/bulk", tags=["students"])
def bulk_delete_students(body: schemas.BulkDeleteRequest, background_tasks: BackgroundTasks):
    """Шаг 2: удаляет студентов по списку id в фоновой задаче."""
    background_tasks.add_task(_bg_bulk_delete_students, body.ids)
    return {"status": "delete scheduled", "ids": body.ids}


@app.delete("/grades/bulk", tags=["grades"])
def bulk_delete_grades(body: schemas.BulkDeleteRequest, background_tasks: BackgroundTasks):
    """Шаг 2: удаляет оценки по списку id в фоновой задаче."""
    background_tasks.add_task(_bg_bulk_delete_grades, body.ids)
    return {"status": "delete scheduled", "ids": body.ids}


# =============================================================================
# faculties CRUD (Шаг 3 — кеш на всех GET)
# =============================================================================

@app.post("/faculties/", response_model=schemas.FacultyOut, tags=["faculties"])
def create_faculty(body: schemas.FacultyCreate, db: Session = Depends(get_db)):
    obj = crud.create_faculty(db, body.name)
    cache.invalidate("faculties:*")
    return obj

@app.get("/faculties/", tags=["faculties"])
def list_faculties(db: Session = Depends(get_db)):
    key = "faculties:all"
    if hit := cache.get(key):
        return hit
    data = [schemas.FacultyOut.model_validate(f).model_dump() for f in crud.list_faculties(db)]
    cache.set(key, data)
    return data

@app.get("/faculties/{faculty_id}", tags=["faculties"])
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    key = f"faculties:{faculty_id}"
    if hit := cache.get(key):
        return hit
    obj = crud.get_faculty(db, faculty_id)
    if not obj:
        raise HTTPException(404, "faculty not found")
    data = schemas.FacultyOut.model_validate(obj).model_dump()
    cache.set(key, data)
    return data

@app.put("/faculties/{faculty_id}", response_model=schemas.FacultyOut, tags=["faculties"])
def update_faculty(faculty_id: int, body: schemas.FacultyUpdate, db: Session = Depends(get_db)):
    obj = crud.update_faculty(db, faculty_id, body.name)
    if not obj:
        raise HTTPException(404, "faculty not found")
    cache.invalidate("faculties:*")
    cache.invalidate("analytics:*")
    return obj

@app.delete("/faculties/{faculty_id}", tags=["faculties"])
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    if not crud.delete_faculty(db, faculty_id):
        raise HTTPException(404, "faculty not found")
    cache.invalidate("faculties:*")
    cache.invalidate("students:*")
    cache.invalidate("grades:*")
    cache.invalidate("analytics:*")
    return {"deleted": faculty_id}


# =============================================================================
# subjects CRUD
# =============================================================================

# /subjects/unique должен быть до /{subject_id} чтобы не пытаться привести "unique" к int
@app.get("/subjects/unique", tags=["subjects"])
def unique_subjects(db: Session = Depends(get_db)):
    key = "subjects:unique"
    if hit := cache.get(key):
        return hit
    data = {"subjects": crud.list_unique_subjects(db)}
    cache.set(key, data)
    return data

@app.post("/subjects/", response_model=schemas.SubjectOut, tags=["subjects"])
def create_subject(body: schemas.SubjectCreate, db: Session = Depends(get_db)):
    obj = crud.create_subject(db, body.name)
    cache.invalidate("subjects:*")
    return obj

@app.get("/subjects/", tags=["subjects"])
def list_subjects(db: Session = Depends(get_db)):
    key = "subjects:all"
    if hit := cache.get(key):
        return hit
    data = [schemas.SubjectOut.model_validate(s).model_dump() for s in crud.list_subjects(db)]
    cache.set(key, data)
    return data

@app.get("/subjects/{subject_id}", tags=["subjects"])
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    key = f"subjects:{subject_id}"
    if hit := cache.get(key):
        return hit
    obj = crud.get_subject(db, subject_id)
    if not obj:
        raise HTTPException(404, "subject not found")
    data = schemas.SubjectOut.model_validate(obj).model_dump()
    cache.set(key, data)
    return data

@app.put("/subjects/{subject_id}", response_model=schemas.SubjectOut, tags=["subjects"])
def update_subject(subject_id: int, body: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    obj = crud.update_subject(db, subject_id, body.name)
    if not obj:
        raise HTTPException(404, "subject not found")
    cache.invalidate("subjects:*")
    return obj

@app.delete("/subjects/{subject_id}", tags=["subjects"])
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    if not crud.delete_subject(db, subject_id):
        raise HTTPException(404, "subject not found")
    cache.invalidate("subjects:*")
    cache.invalidate("grades:*")
    cache.invalidate("analytics:*")
    return {"deleted": subject_id}


# =============================================================================
# students CRUD
# =============================================================================

@app.post("/students/", response_model=schemas.StudentOut, tags=["students"])
def create_student(body: schemas.StudentCreate, db: Session = Depends(get_db)):
    obj = crud.create_student(db, body.last_name, body.first_name)
    cache.invalidate("students:*")
    return obj

@app.get("/students/", tags=["students"])
def list_students(
    faculty: str = Query(None, description="фильтр по факультету"),
    db: Session = Depends(get_db)
):
    key = f"students:list:{faculty or 'all'}"
    if hit := cache.get(key):
        return hit
    raw = crud.list_students_by_faculty(db, faculty) if faculty else crud.list_students(db)
    data = [schemas.StudentOut.model_validate(s).model_dump() for s in raw]
    cache.set(key, data)
    return data

@app.get("/students/low-grades", tags=["students"])
def students_low_grades(
    subject: str = Query(..., description="название курса"),
    threshold: int = Query(30),
    db: Session = Depends(get_db)
):
    key = f"students:low:{subject}:{threshold}"
    if hit := cache.get(key):
        return hit
    rows = crud.list_students_low_grade(db, subject, threshold)
    data = [
        {"student": schemas.StudentOut.model_validate(r["student"]).model_dump(), "grade": r["grade"]}
        for r in rows
    ]
    cache.set(key, data)
    return data

@app.get("/students/{student_id}", tags=["students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    key = f"students:{student_id}"
    if hit := cache.get(key):
        return hit
    obj = crud.get_student(db, student_id)
    if not obj:
        raise HTTPException(404, "student not found")
    data = schemas.StudentOut.model_validate(obj).model_dump()
    cache.set(key, data)
    return data

@app.put("/students/{student_id}", response_model=schemas.StudentOut, tags=["students"])
def update_student(student_id: int, body: schemas.StudentUpdate, db: Session = Depends(get_db)):
    obj = crud.update_student(db, student_id, body.last_name, body.first_name)
    if not obj:
        raise HTTPException(404, "student not found")
    cache.invalidate("students:*")
    return obj

@app.delete("/students/{student_id}", tags=["students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(404, "student not found")
    cache.invalidate("students:*")
    cache.invalidate("grades:*")
    return {"deleted": student_id}


# =============================================================================
# grades CRUD
# =============================================================================

@app.post("/grades/", response_model=schemas.GradeOut, tags=["grades"])
def create_grade(body: schemas.GradeCreate, db: Session = Depends(get_db)):
    obj = crud.create_grade(db, body.student_id, body.faculty_id, body.subject_id, body.grade)
    cache.invalidate("grades:*")
    cache.invalidate("analytics:*")
    cache.invalidate("students:low*")
    return obj

@app.get("/grades/", tags=["grades"])
def list_grades(db: Session = Depends(get_db)):
    key = "grades:all"
    if hit := cache.get(key):
        return hit
    data = [schemas.GradeOut.model_validate(g).model_dump() for g in crud.list_grades(db)]
    cache.set(key, data)
    return data

@app.get("/grades/{grade_id}", tags=["grades"])
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    key = f"grades:{grade_id}"
    if hit := cache.get(key):
        return hit
    obj = crud.get_grade(db, grade_id)
    if not obj:
        raise HTTPException(404, "grade not found")
    data = schemas.GradeOut.model_validate(obj).model_dump()
    cache.set(key, data)
    return data

@app.put("/grades/{grade_id}", response_model=schemas.GradeOut, tags=["grades"])
def update_grade(grade_id: int, body: schemas.GradeUpdate, db: Session = Depends(get_db)):
    obj = crud.update_grade(db, grade_id, body.grade)
    if not obj:
        raise HTTPException(404, "grade not found")
    cache.invalidate("grades:*")
    cache.invalidate("analytics:*")
    cache.invalidate("students:low*")
    return obj

@app.delete("/grades/{grade_id}", tags=["grades"])
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    if not crud.delete_grade(db, grade_id):
        raise HTTPException(404, "grade not found")
    cache.invalidate("grades:*")
    cache.invalidate("analytics:*")
    return {"deleted": grade_id}


# =============================================================================
# analytics
# =============================================================================

@app.get("/analytics/avg-grade", tags=["analytics"])
def avg_grade_by_faculty(
    faculty: str = Query(..., description="название факультета"),
    db: Session = Depends(get_db)
):
    key = f"analytics:avg:{faculty}"
    if hit := cache.get(key):
        return hit
    avg = crud.avg_grade_by_faculty(db, faculty)
    if avg is None:
        raise HTTPException(404, "faculty not found or no grades")
    data = {"faculty": faculty, "avg_grade": avg}
    cache.set(key, data)
    return data


# =============================================================================
# export
# =============================================================================

@app.get("/export/csv", tags=["data"])
def export_csv(db: Session = Depends(get_db)):
    content = crud.export_to_csv(db)
    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students_export.csv"}
    )
