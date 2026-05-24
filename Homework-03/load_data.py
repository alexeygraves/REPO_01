import csv
from database import SessionLocal, engine
from models import Base, Faculty, Subject, Student, Grade

Base.metadata.create_all(engine)


def get_or_create(session, model, **kwargs):
    obj = session.query(model).filter_by(**kwargs).first()
    if not obj:
        obj = model(**kwargs)
        session.add(obj)
        session.flush()
    return obj


def load(filepath="students.csv"):
    session = SessionLocal()
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("Фамилия"):
                    continue

                faculty = get_or_create(session, Faculty, name=row["Факультет"].strip())
                subject = get_or_create(session, Subject, name=row["Курс"].strip())
                student = get_or_create(
                    session, Student,
                    last_name=row["Фамилия"].strip(),
                    first_name=row["Имя"].strip()
                )

                grade = Grade(
                    student_id=student.id,
                    faculty_id=faculty.id,
                    subject_id=subject.id,
                    grade=int(row["Оценка"])
                )
                session.add(grade)

        session.commit()
        print("data loaded ok")
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    load()
