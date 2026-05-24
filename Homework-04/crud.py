import csv
from io import StringIO
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Faculty, Subject, Student, Grade


# --- helpers ---

def _get_or_create(session, model, **kwargs):
    obj = session.query(model).filter_by(**kwargs).first()
    if not obj:
        obj = model(**kwargs)
        session.add(obj)
        session.flush()
    return obj


# === Faculty ===

def get_faculty(db: Session, faculty_id: int):
    return db.query(Faculty).filter(Faculty.id == faculty_id).first()

def get_faculty_by_name(db: Session, name: str):
    return db.query(Faculty).filter(Faculty.name == name).first()

def list_faculties(db: Session):
    return db.query(Faculty).all()

def create_faculty(db: Session, name: str):
    obj = Faculty(name=name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_faculty(db: Session, faculty_id: int, name: str):
    obj = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not obj:
        return None
    obj.name = name
    db.commit()
    db.refresh(obj)
    return obj

def delete_faculty(db: Session, faculty_id: int) -> bool:
    obj = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# === Subject ===

def get_subject(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()

def list_subjects(db: Session):
    return db.query(Subject).all()

def list_unique_subjects(db: Session):
    return [r[0] for r in db.query(Subject.name).distinct().all()]

def create_subject(db: Session, name: str):
    obj = Subject(name=name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_subject(db: Session, subject_id: int, name: str):
    obj = db.query(Subject).filter(Subject.id == subject_id).first()
    if not obj:
        return None
    obj.name = name
    db.commit()
    db.refresh(obj)
    return obj

def delete_subject(db: Session, subject_id: int) -> bool:
    obj = db.query(Subject).filter(Subject.id == subject_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# === Student ===

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def list_students(db: Session):
    return db.query(Student).all()

def list_students_by_faculty(db: Session, faculty_name: str):
    return (
        db.query(Student)
        .join(Grade, Grade.student_id == Student.id)
        .join(Faculty, Faculty.id == Grade.faculty_id)
        .filter(Faculty.name == faculty_name)
        .distinct()
        .all()
    )

def list_students_low_grade(db: Session, subject_name: str, threshold: int = 30):
    rows = (
        db.query(Student, Grade.grade)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name, Grade.grade < threshold)
        .all()
    )
    return [{"student": s, "grade": g} for s, g in rows]

def create_student(db: Session, last_name: str, first_name: str):
    obj = Student(last_name=last_name, first_name=first_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_student(db: Session, student_id: int, last_name: str = None, first_name: str = None):
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        return None
    if last_name is not None:
        obj.last_name = last_name
    if first_name is not None:
        obj.first_name = first_name
    db.commit()
    db.refresh(obj)
    return obj

def delete_student(db: Session, student_id: int) -> bool:
    obj = db.query(Student).filter(Student.id == student_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# === Grade ===

def get_grade(db: Session, grade_id: int):
    return db.query(Grade).filter(Grade.id == grade_id).first()

def list_grades(db: Session):
    return db.query(Grade).all()

def create_grade(db: Session, student_id: int, faculty_id: int, subject_id: int, grade: int):
    obj = Grade(student_id=student_id, faculty_id=faculty_id, subject_id=subject_id, grade=grade)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_grade(db: Session, grade_id: int, grade: int):
    obj = db.query(Grade).filter(Grade.id == grade_id).first()
    if not obj:
        return None
    obj.grade = grade
    db.commit()
    db.refresh(obj)
    return obj

def delete_grade(db: Session, grade_id: int) -> bool:
    obj = db.query(Grade).filter(Grade.id == grade_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# === Analytics ===

def avg_grade_by_faculty(db: Session, faculty_name: str):
    result = (
        db.query(func.avg(Grade.grade))
        .join(Faculty, Faculty.id == Grade.faculty_id)
        .filter(Faculty.name == faculty_name)
        .scalar()
    )
    return round(float(result), 2) if result is not None else None


# === CSV import / export ===

def load_from_csv(db: Session, filepath: str = "students.csv"):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("Фамилия"):
                continue
            faculty = _get_or_create(db, Faculty, name=row["Факультет"].strip())
            subject = _get_or_create(db, Subject, name=row["Курс"].strip())
            student = _get_or_create(
                db, Student,
                last_name=row["Фамилия"].strip(),
                first_name=row["Имя"].strip()
            )
            db.add(Grade(
                student_id=student.id,
                faculty_id=faculty.id,
                subject_id=subject.id,
                grade=int(row["Оценка"])
            ))
    db.commit()


def export_to_csv(db: Session) -> str:
    rows = (
        db.query(
            Student.last_name,
            Student.first_name,
            Faculty.name.label("faculty"),
            Subject.name.label("subject"),
            Grade.grade
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Faculty, Faculty.id == Grade.faculty_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .all()
    )
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Фамилия", "Имя", "Факультет", "Курс", "Оценка"])
    for r in rows:
        writer.writerow([r.last_name, r.first_name, r.faculty, r.subject, r.grade])
    return buf.getvalue()
